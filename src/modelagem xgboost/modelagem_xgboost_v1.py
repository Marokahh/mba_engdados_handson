import sys
from pathlib import Path

import pandas as pd
from psycopg2 import sql

from xgboost import XGBClassifier

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

# Tamanho da amostra utilizada no XGBoost V1
TAMANHO_AMOSTRA = 200_000

# Variável que queremos prever
TARGET = "TP_PRESENCA_CN"


# ============================================================
# VARIÁVEIS UTILIZADAS PELO MODELO
# ============================================================

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
    print("XGBOOST V1 - PREVISÃO DE AUSÊNCIA NO ENEM")
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

        colunas_banco = {
            linha[0]
            for linha in cursor.fetchall()
        }

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
                "Nenhuma das variáveis selecionadas "
                "foi encontrada na tabela."
            )

        # ====================================================
        # 3. BUSCAR A MESMA AMOSTRA SEMPRE
        # ====================================================

        print("\n" + "-" * 80)
        print("CARREGANDO DADOS")
        print("-" * 80)

        print(
            f"\nSerá utilizada uma amostra fixa de "
            f"{TAMANHO_AMOSTRA:,} registros."
        )

        print(
            "A mesma amostra será utilizada em todas as execuções."
        )

        # ----------------------------------------------------
        # Monta lista de colunas
        # ----------------------------------------------------

        colunas_sql_lista = [
            TARGET
        ] + variaveis_disponiveis

        # Remove possíveis duplicações
        colunas_sql_lista = list(
            dict.fromkeys(colunas_sql_lista)
        )

        # ----------------------------------------------------
        # Verifica se existe NU_INSCRICAO
        # ----------------------------------------------------

        if "NU_INSCRICAO" in colunas_banco:

            ordem_amostra = sql.Identifier(
                "NU_INSCRICAO"
            )

        else:

            # Caso NU_INSCRICAO não exista,
            # utiliza as próprias variáveis do modelo
            # para criar uma ordem determinística.
            ordem_amostra = sql.SQL(
                "CONCAT_WS('|', "
                + ", ".join(
                    f'"{coluna}"::text'
                    for coluna in variaveis_disponiveis
                )
                + ")"
            )

        # ----------------------------------------------------
        # Monta SELECT com identificadores protegidos
        # ----------------------------------------------------

        colunas_sql = sql.SQL(", ").join(
            sql.Identifier(coluna)
            for coluna in colunas_sql_lista
        )

        consulta = sql.SQL(
            """
            SELECT {colunas}
            FROM {tabela}
            WHERE {target} IN (0, 1)
            ORDER BY {ordem}
            LIMIT {limite};
            """
        ).format(

            colunas=colunas_sql,

            tabela=sql.SQL(
                TABELA
            ),

            target=sql.Identifier(
                TARGET
            ),

            ordem=ordem_amostra,

            limite=sql.Literal(
                TAMANHO_AMOSTRA
            )
        )

        consulta = consulta.as_string(conn)

        df = pd.read_sql_query(
            consulta,
            conn
        )

        print(
            f"Registros carregados: "
            f"{len(df):,}"
        )

        # ====================================================
        # 4. TRATAMENTO DOS DADOS
        # ====================================================

        print("\n" + "-" * 80)
        print("TRATAMENTO DOS DADOS")
        print("-" * 80)

        # Remove registros sem variável alvo
        df = df.dropna(
            subset=[TARGET]
        )

        # Converte variável alvo para inteiro
        df[TARGET] = df[TARGET].astype(int)

        print(
            f"Registros após tratamento: "
            f"{len(df):,}"
        )

        # ====================================================
        # 5. SEPARAÇÃO ENTRE X E Y
        # ====================================================

        X = df[
            variaveis_disponiveis
        ].copy()

        y = df[
            TARGET
        ].copy()

        # ====================================================
        # 6. TRATAMENTO DOS VALORES AUSENTES
        # ====================================================

        for coluna in X.columns:

            if X[coluna].dtype == "object":

                X[coluna] = X[coluna].fillna(
                    "MISSING"
                )

            else:

                X[coluna] = X[coluna].fillna(
                    -1
                )

        # ====================================================
        # 7. TRANSFORMAÇÃO DAS VARIÁVEIS CATEGÓRICAS
        # ====================================================

        print(
            "\nTransformando variáveis categóricas..."
        )

        X = pd.get_dummies(
            X,
            dtype=int
        )

        print(
            f"Quantidade de variáveis após transformação: "
            f"{X.shape[1]}"
        )

        # ====================================================
        # 8. TREINO E TESTE
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

        print(
            f"Treino: {len(X_train):,}"
        )

        print(
            f"Teste : {len(X_test):,}"
        )

        # ====================================================
        # 9. CÁLCULO DO BALANCEAMENTO
        # ====================================================

        quantidade_presentes = (
            y_train == 0
        ).sum()

        quantidade_ausentes = (
            y_train == 1
        ).sum()

        if quantidade_ausentes > 0:

            scale_pos_weight = (
                quantidade_presentes
                / quantidade_ausentes
            )

        else:

            scale_pos_weight = 1

        print("\nBalanceamento das classes:")

        print(
            f" - Presentes: "
            f"{quantidade_presentes:,}"
        )

        print(
            f" - Ausentes : "
            f"{quantidade_ausentes:,}"
        )

        print(
            f" - scale_pos_weight = "
            f"{scale_pos_weight:.4f}"
        )

        # ====================================================
        # 10. XGBOOST
        # ====================================================

        print("\n" + "-" * 80)
        print("TREINANDO XGBOOST V1")
        print("-" * 80)

        print("\nParâmetros:")

        print(" - n_estimators = 200")
        print(" - max_depth = 6")
        print(" - learning_rate = 0.10")
        print(" - subsample = 0.80")
        print(" - colsample_bytree = 0.80")
        print(" - tree_method = hist")
        print(" - random_state = 42")

        modelo = XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.10,
            subsample=0.80,
            colsample_bytree=0.80,
            tree_method="hist",
            random_state=42,
            n_jobs=-1,
            scale_pos_weight=scale_pos_weight,
            eval_metric="logloss"
        )

        modelo.fit(
            X_train,
            y_train
        )

        print(
            "\nModelo treinado com sucesso."
        )

        # ====================================================
        # 11. PREVISÕES
        # ====================================================

        print("\n" + "-" * 80)
        print("REALIZANDO PREVISÕES")
        print("-" * 80)

        y_pred = modelo.predict(
            X_test
        )

        print(
            "Previsões realizadas com sucesso."
        )

        # ====================================================
        # 12. MÉTRICAS
        # ====================================================

        accuracy = accuracy_score(
            y_test,
            y_pred
        )

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
        # 13. MATRIZ DE CONFUSÃO
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

        # ====================================================
        # 14. ESPECIFICIDADE
        # ====================================================

        if (
            verdadeiro_negativo
            + falso_positivo
            > 0
        ):

            especificidade = (
                verdadeiro_negativo
                /
                (
                    verdadeiro_negativo
                    + falso_positivo
                )
            )

        else:

            especificidade = 0

        # ====================================================
        # 15. RESULTADOS
        # ====================================================

        print("\n" + "=" * 80)
        print("MÉTRICAS DO XGBOOST V1")
        print("=" * 80)

        print(
            f"\nAccuracy           : "
            f"{accuracy:.4f} "
            f"({accuracy:.2%})"
        )

        print(
            f"Precision (Ausente): "
            f"{precision:.4f}"
        )

        print(
            f"Recall (Ausente)   : "
            f"{recall:.4f}"
        )

        print(
            f"F1-score (Ausente) : "
            f"{f1:.4f}"
        )

        print(
            f"Especificidade     : "
            f"{especificidade:.4f}"
        )

        print(
            f"Balanced Accuracy  : "
            f"{balanced_accuracy:.4f}"
        )

        # ====================================================
        # 16. MATRIZ DE CONFUSÃO
        # ====================================================

        print("\n" + "-" * 80)
        print("MATRIZ DE CONFUSÃO")
        print("-" * 80)

        print("\n                    PREVISTO")
        print("                 Presente  Ausente")

        print(
            f"REAL Presente   "
            f"{verdadeiro_negativo:>10,}  "
            f"{falso_positivo:>8,}"
        )

        print(
            f"     Ausente    "
            f"{falso_negativo:>10,}  "
            f"{verdadeiro_positivo:>8,}"
        )

        # ====================================================
        # 17. CONCLUSÃO
        # ====================================================

        print("\n" + "=" * 80)
        print("CONCLUSÃO DO XGBOOST V1")
        print("=" * 80)

        print(
            f"\nO XGBoost V1 apresentou Recall de "
            f"{recall:.2%} para a classe Ausente."
        )

        print(
            f"F1-score para Ausente: "
            f"{f1:.2%}."
        )

        print(
            f"Balanced Accuracy: "
            f"{balanced_accuracy:.2%}."
        )

        print(
            "\nA versão V1 utiliza uma amostra fixa "
            "de 200.000 registros."
        )

        print(
            "A mesma amostra é utilizada em todas "
            "as execuções do modelo."
        )

        print(
            "\nEsses resultados serão comparados "
            "com o baseline, Random Forest e "
            "versões posteriores do XGBoost."
        )

    finally:

        conn.close()

        print(
            "\nConexão com PostgreSQL encerrada."
        )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()


# ============================================================
# INFORMAÇÕES DO MODELO
# ============================================================

# XGBoost V1:
#
# Treinado utilizando uma amostra fixa de 200.000 registros
# da base tratada, com 80% dos dados destinados ao treinamento
# e 20% ao teste.
#
# A classe 1 representa os participantes ausentes.
#
# As métricas utilizadas são:
# Accuracy, Precision, Recall, F1-score,
# Especificidade e Balanced Accuracy.
#
# Os resultados serão comparados com o baseline,
# Random Forest e versões posteriores do XGBoost.