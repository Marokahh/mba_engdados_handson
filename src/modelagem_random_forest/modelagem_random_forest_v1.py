import sys
from pathlib import Path

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    balanced_accuracy_score
)


# ============================================================
# CONFIGURAÇÃO DOS CAMINHOS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "src"

# Permite importar os módulos do projeto
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from src.database import get_connection


# ============================================================
# CONFIGURAÇÕES DO MODELO
# ============================================================

TABELA = "dw_enem.microdados_enem_tratado"

# Tamanho da amostra usada para treinar o modelo.
# A tabela possui mais de 21 milhões de registros.
TAMANHO_AMOSTRA = 200_000

# Variável que queremos prever
TARGET = "TP_PRESENCA_CN"


# Variáveis que podem ser usadas pelo modelo.
# O código verifica quais realmente existem na tabela.
VARIAVEIS = [
    "NU_IDADE",
    "TP_SEXO",
    "TP_COR_RACA",
    "TP_ESTADO_CIVIL",
    "TP_NACIONALIDADE",
    "TP_ESCOLA",
    "TP_ENSINO",
    "IN_TREINEIRO",
    "TP_ST_CONCLUSAO",
    "TP_ANO_CONCLUIU",
    "TP_LOCALIZACAO_ESC",
    "TP_DEPENDENCIA_ADM_ESC",
    "TP_SIT_FUNC_ESC"
]


def main():

    print("\n" + "=" * 80)
    print("RANDOM FOREST - PREVISÃO DE AUSÊNCIA NO ENEM")
    print("=" * 80)

    # ========================================================
    # 1. CONEXÃO COM O BANCO
    # ========================================================

    conn = get_connection()

    try:

        print("\nConexão com PostgreSQL realizada.")

        # ====================================================
        # 2. DESCOBRIR QUAIS VARIÁVEIS EXISTEM
        # ====================================================

        print("\n" + "-" * 80)
        print("VERIFICANDO VARIÁVEIS")
        print("-" * 80)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'dw_enem'
              AND table_name = 'microdados_enem_tratado';
            """
        )

        colunas_banco = {linha[0] for linha in cursor.fetchall()}

        # Mantém somente as variáveis que realmente existem
        variaveis_disponiveis = [
            coluna
            for coluna in VARIAVEIS
            if coluna in colunas_banco
        ]

        print("\nVariáveis encontradas:")

        for coluna in variaveis_disponiveis:
            print(f" - {coluna}")

        if not variaveis_disponiveis:
            raise Exception(
                "Nenhuma das variáveis selecionadas foi encontrada na tabela."
            )

        # ====================================================
        # 3. BUSCAR UMA AMOSTRA
        # ====================================================

        print("\n" + "-" * 80)
        print("CARREGANDO DADOS")
        print("-" * 80)

        print(
            f"\nSerá utilizada uma amostra de "
            f"{TAMANHO_AMOSTRA:,} registros."
        )

        colunas_sql = [TARGET] + variaveis_disponiveis

        colunas_sql = list(dict.fromkeys(colunas_sql))

        consulta = f"""
            SELECT
                {", ".join(f'"{coluna}"' for coluna in colunas_sql)}
            FROM {TABELA}
            WHERE "{TARGET}" IN (0, 1)
            LIMIT {TAMANHO_AMOSTRA};
        """

        df = pd.read_sql_query(consulta, conn)

        print(f"Registros carregados: {len(df):,}")

        # ====================================================
        # 4. TRATAMENTO DOS DADOS
        # ====================================================

        print("\n" + "-" * 80)
        print("TRATAMENTO DOS DADOS")
        print("-" * 80)

        # Remove registros sem variável alvo
        df = df.dropna(subset=[TARGET])

        # Converte a variável alvo para inteiro
        df[TARGET] = df[TARGET].astype(int)

        print(f"Registros após tratamento: {len(df):,}")

        # ====================================================
        # 5. SEPARAÇÃO ENTRE X E Y
        # ====================================================

        X = df[variaveis_disponiveis].copy()
        y = df[TARGET].copy()

        # Preenche valores ausentes
        for coluna in X.columns:

            if X[coluna].dtype == "object":
                X[coluna] = X[coluna].fillna("MISSING")
            else:
                X[coluna] = X[coluna].fillna(-1)

        # ====================================================
        # 6. TRANSFORMAÇÃO DAS VARIÁVEIS CATEGÓRICAS
        # ====================================================

        print("\nTransformando variáveis categóricas...")

        # Converte automaticamente textos como F, M, etc.
        # em variáveis numéricas que o Random Forest consegue usar.
        X = pd.get_dummies(
            X,
            dtype=int
        )

        print(f"Quantidade de variáveis após transformação: {X.shape[1]}")

        # ====================================================
        # 7. TREINO E TESTE
        # ====================================================

        print("\n" + "-" * 80)
        print("SEPARAÇÃO TREINO / TESTE")
        print("-" * 80)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

        print(f"Treino: {len(X_train):,}")
        print(f"Teste : {len(X_test):,}")

        # ====================================================
        # 8. RANDOM FOREST
        # ====================================================

        print("\n" + "-" * 80)
        print("TREINANDO RANDOM FOREST")
        print("-" * 80)

        print("\nParâmetros:")
        print(" - n_estimators = 100")
        print(" - max_depth = 15")
        print(" - random_state = 42")
        print(" - class_weight = balanced")

        modelo = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        )

        modelo.fit(X_train, y_train)

        print("\nModelo treinado com sucesso.")

        # ====================================================
        # 9. PREVISÕES
        # ====================================================

        print("\n" + "-" * 80)
        print("REALIZANDO PREVISÕES")
        print("-" * 80)

        y_pred = modelo.predict(X_test)

        # ====================================================
        # 10. MÉTRICAS
        # ====================================================

        accuracy = accuracy_score(y_test, y_pred)

        precision = precision_score(
            y_test,
            y_pred,
            pos_label=1,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            y_pred,
            pos_label=1,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            y_pred,
            pos_label=1,
            zero_division=0
        )

        balanced_accuracy = balanced_accuracy_score(
            y_test,
            y_pred
        )

        # ====================================================
        # 11. MATRIZ DE CONFUSÃO
        # ====================================================

        matriz = confusion_matrix(
            y_test,
            y_pred,
            labels=[0, 1]
        )

        verdadeiro_negativo = matriz[0][0]
        falso_positivo = matriz[0][1]
        falso_negativo = matriz[1][0]
        verdadeiro_positivo = matriz[1][1]

        # Especificidade
        if verdadeiro_negativo + falso_positivo > 0:

            especificidade = (
                verdadeiro_negativo
                / (verdadeiro_negativo + falso_positivo)
            )

        else:

            especificidade = 0

        # ====================================================
        # 12. RESULTADOS
        # ====================================================

        print("\n" + "=" * 80)
        print("MÉTRICAS DO RANDOM FOREST")
        print("=" * 80)

        print(f"\nAccuracy           : {accuracy:.4f} ({accuracy:.2%})")
        print(f"Precision (Ausente): {precision:.4f}")
        print(f"Recall (Ausente)   : {recall:.4f}")
        print(f"F1-score (Ausente) : {f1:.4f}")
        print(f"Especificidade     : {especificidade:.4f}")
        print(f"Balanced Accuracy  : {balanced_accuracy:.4f}")

        # ====================================================
        # 13. MATRIZ DE CONFUSÃO
        # ====================================================

        print("\n" + "-" * 80)
        print("MATRIZ DE CONFUSÃO")
        print("-" * 80)

        print("\n                    PREVISTO")
        print("                 Presente  Ausente")

        print(
            f"REAL Presente   {verdadeiro_negativo:>10,}  "
            f"{falso_positivo:>8,}"
        )

        print(
            f"     Ausente    {falso_negativo:>10,}  "
            f"{verdadeiro_positivo:>8,}"
        )

        # ====================================================
        # 14. CONCLUSÃO
        # ====================================================

        print("\n" + "=" * 80)
        print("CONCLUSÃO DO RANDOM FOREST")
        print("=" * 80)

        print(
            f"\nO Random Forest apresentou Recall de "
            f"{recall:.2%} para a classe Ausente."
        )

        print(
            f"F1-score para Ausente: {f1:.2%}."
        )

        print(
            f"Balanced Accuracy: {balanced_accuracy:.2%}."
        )

        print(
            "\nEsses resultados serão comparados posteriormente "
            "com o baseline e com os próximos modelos."
        )

    finally:

        conn.close()

        print("\nConexão com PostgreSQL encerrada.")


if __name__ == "__main__":
    main()

# Random Forest V1: foi treinado utilizando uma amostra de 200.000 registros da base tratada, com 80% dos dados destinados ao treinamento e 20% ao teste. A classe 1 representa os participantes ausentes.
# O modelo apresentou Accuracy de 61,43%, Precision de 84,79%, Recall de 59,84%, F1-score de 70,16% e Balanced Accuracy de 63,12%.
# Em comparação ao baseline, que apresentou Recall e F1-score de 0% para a classe Ausente, o Random Forest demonstrou capacidade de identificar padrões associados à ausência. 
# Por esse motivo, a avaliação dos próximos modelos será realizada utilizando as mesmas métricas, com atenção especial ao Recall, F1-score e Balanced Accuracy.