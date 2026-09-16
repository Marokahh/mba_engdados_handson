import sys
import gc
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

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from src.database import get_connection


# ============================================================
# CONFIGURAÇÕES
# ============================================================

TABELA = "dw_enem.microdados_enem_tratado"
TARGET = "TP_PRESENCA_CN"


# ------------------------------------------------------------
# Quantidade de registros utilizados no treinamento.
#
# A base é lida em blocos para não colocar todos os
# registros na memória ao mesmo tempo.
# ------------------------------------------------------------

MAX_REGISTROS_MODELO = 2_100_000

# Tamanho de cada leitura do PostgreSQL
TAMANHO_CHUNK = 100_000


# ------------------------------------------------------------
# Variáveis utilizadas pelo modelo
# ------------------------------------------------------------

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


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main():

    print("\n" + "=" * 80)
    print("RANDOM FOREST V2 - PREVISÃO DE AUSÊNCIA NO ENEM")
    print("=" * 80)

    conn = get_connection()

    try:

        print("\nConexão com PostgreSQL realizada.")

        # ====================================================
        # 1. VERIFICAR VARIÁVEIS
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
                "Nenhuma das variáveis selecionadas foi encontrada."
            )

        # ====================================================
        # 2. CONTAR REGISTROS DA BASE
        # ====================================================

        print("\n" + "-" * 80)
        print("VERIFICANDO TAMANHO DA BASE")
        print("-" * 80)

        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM {TABELA}
            WHERE "{TARGET}" IN (0, 1);
            """
        )

        total_registros = cursor.fetchone()[0]

        print(
            f"\nRegistros disponíveis para o modelo: "
            f"{total_registros:,}"
        )

        print(
            f"Limite de registros utilizados: "
            f"{MAX_REGISTROS_MODELO:,}"
        )

        print(
            f"Tamanho de cada bloco: "
            f"{TAMANHO_CHUNK:,}"
        )

        # ====================================================
        # 3. CONSULTA
        # ====================================================

        colunas_sql = [TARGET] + variaveis_disponiveis

        # Remove possíveis duplicações
        colunas_sql = list(dict.fromkeys(colunas_sql))

        # ----------------------------------------------------
        # ORDER BY garante que as mesmas linhas sejam
        # selecionadas em todas as execuções.
        # ----------------------------------------------------

        consulta = f"""
            SELECT
                {", ".join(f'"{coluna}"' for coluna in colunas_sql)}
            FROM {TABELA}
            WHERE "{TARGET}" IN (0, 1)
            ORDER BY "NU_INSCRICAO";
        """

        # ====================================================
        # 4. LEITURA EM BLOCOS
        # ====================================================

        print("\n" + "-" * 80)
        print("LENDO A BASE EM BLOCOS")
        print("-" * 80)

        print(
            "\nA base será percorrida em blocos de "
            f"{TAMANHO_CHUNK:,} registros."
        )

        print(
            "Serão mantidos até "
            f"{MAX_REGISTROS_MODELO:,} registros para o modelo."
        )

        chunks = []

        registros_lidos = 0
        registros_mantidos = 0
        numero_chunk = 0

        for chunk in pd.read_sql_query(
            consulta,
            conn,
            chunksize=TAMANHO_CHUNK
        ):

            numero_chunk += 1
            registros_lidos += len(chunk)

            # ----------------------------------------------
            # Remove registros sem variável alvo
            # ----------------------------------------------

            chunk = chunk.dropna(
                subset=[TARGET]
            )

            chunk[TARGET] = chunk[TARGET].astype("int8")

            # ----------------------------------------------
            # Quantidade que ainda podemos guardar
            # ----------------------------------------------

            quantidade_restante = (
                MAX_REGISTROS_MODELO - registros_mantidos
            )

            if quantidade_restante <= 0:
                break

            # ----------------------------------------------
            # Caso o último chunk ultrapasse o limite,
            # pega somente a quantidade necessária.
            # ----------------------------------------------

            if len(chunk) > quantidade_restante:

                chunk = chunk.iloc[
                    :quantidade_restante
                ].copy()

            chunks.append(chunk)

            registros_mantidos += len(chunk)

            percentual = (
                registros_lidos / total_registros
            ) * 100

            if percentual > 100:
                percentual = 100

            print(
                f"Chunk {numero_chunk:>3} | "
                f"Lidos: {registros_lidos:>12,} | "
                f"Memória: {registros_mantidos:>10,} | "
                f"Progresso: {percentual:>6.2f}%"
            )

            # ----------------------------------------------
            # Se atingiu o limite, para a leitura.
            # ----------------------------------------------

            if registros_mantidos >= MAX_REGISTROS_MODELO:
                break

            del chunk
            gc.collect()

        # ====================================================
        # 5. JUNTAR OS DADOS
        # ====================================================

        print("\n" + "-" * 80)
        print("PREPARANDO DADOS PARA O MODELO")
        print("-" * 80)

        df = pd.concat(
            chunks,
            ignore_index=True
        )

        del chunks
        gc.collect()

        print(
            f"\nRegistros separados para o modelo: "
            f"{len(df):,}"
        )

        # ====================================================
        # 6. SEPARAÇÃO X E Y
        # ====================================================

        X = df[variaveis_disponiveis].copy()
        y = df[TARGET].copy()

        del df
        gc.collect()

        # ====================================================
        # 7. TRATAMENTO
        # ====================================================

        print("\n" + "-" * 80)
        print("TRATANDO OS DADOS")
        print("-" * 80)

        for coluna in X.columns:

            if X[coluna].dtype == "object":

                X[coluna] = X[coluna].fillna(
                    "MISSING"
                )

            else:

                X[coluna] = X[coluna].fillna(-1)

        print(
            "\nVariáveis categóricas sendo transformadas..."
        )

        X = pd.get_dummies(
            X,
            dtype="int8"
        )

        print(
            f"Quantidade de variáveis após transformação: "
            f"{X.shape[1]}"
        )

        # ====================================================
        # 8. SEPARAÇÃO TREINO / TESTE
        # ====================================================

        print("\n" + "-" * 80)
        print("SEPARANDO TREINO E TESTE")
        print("-" * 80)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

        print(
            f"\nTreino: {len(X_train):,}"
        )

        print(
            f"Teste : {len(X_test):,}"
        )

        # ====================================================
        # 9. RANDOM FOREST
        # ====================================================

        print("\n" + "-" * 80)
        print("TREINANDO RANDOM FOREST V2")
        print("-" * 80)

        print("\nParâmetros:")

        print(" - n_estimators = 100")
        print(" - max_depth = 15")
        print(" - random_state = 42")
        print(" - class_weight = balanced")
        print(" - n_jobs = -1")

        print(
            "\nO treinamento pode levar alguns minutos."
        )

        modelo = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        )

        modelo.fit(
            X_train,
            y_train
        )

        print("\nModelo treinado com sucesso.")

        # ====================================================
        # 10. PREVISÕES
        # ====================================================

        print("\n" + "-" * 80)
        print("REALIZANDO PREVISÕES")
        print("-" * 80)

        y_pred = modelo.predict(
            X_test
        )

        # ====================================================
        # 11. MÉTRICAS
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
        # 12. MATRIZ DE CONFUSÃO
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

        # ----------------------------------------------------
        # Especificidade
        # ----------------------------------------------------

        if verdadeiro_negativo + falso_positivo > 0:

            especificidade = (
                verdadeiro_negativo
                /
                (
                    verdadeiro_negativo
                    +
                    falso_positivo
                )
            )

        else:

            especificidade = 0

        # ====================================================
        # 13. RESULTADOS
        # ====================================================

        print("\n" + "=" * 80)
        print("MÉTRICAS DO RANDOM FOREST V2")
        print("=" * 80)

        print(
            f"\nAccuracy            : "
            f"{accuracy:.4f} ({accuracy:.2%})"
        )

        print(
            f"Precision (Ausente) : "
            f"{precision:.4f} ({precision:.2%})"
        )

        print(
            f"Recall (Ausente)    : "
            f"{recall:.4f} ({recall:.2%})"
        )

        print(
            f"F1-score (Ausente)  : "
            f"{f1:.4f} ({f1:.2%})"
        )

        print(
            f"Especificidade      : "
            f"{especificidade:.4f} ({especificidade:.2%})"
        )

        print(
            f"Balanced Accuracy   : "
            f"{balanced_accuracy:.4f} "
            f"({balanced_accuracy:.2%})"
        )

        # ====================================================
        # 14. MATRIZ DE CONFUSÃO
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
        # 15. CONCLUSÃO
        # ====================================================

        print("\n" + "=" * 80)
        print("CONCLUSÃO DO RANDOM FOREST V2")
        print("=" * 80)

        print(
            f"\nO modelo foi treinado utilizando "
            f"{len(X_train):,} registros."
        )

        print(
            f"Recall para Ausente: "
            f"{recall:.2%}"
        )

        print(
            f"F1-score para Ausente: "
            f"{f1:.2%}"
        )

        print(
            f"Balanced Accuracy: "
            f"{balanced_accuracy:.2%}"
        )

        print(
            "\nO Random Forest V2 será utilizado "
            "para comparação com os próximos modelos."
        )

        # ====================================================
        # 16. LIBERAR MEMÓRIA
        # ====================================================

        del X
        del y
        del X_train
        del X_test
        del y_train
        del y_test
        del y_pred
        del modelo

        gc.collect()

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


# Random Forest V2:
# Foi treinado utilizando aproximadamente 10% dos registros
# da base tratada.
#
# A leitura é feita em blocos de 100 mil registros.
# A seleção é ordenada por NU_INSCRICAO para garantir
# que o mesmo conjunto de 2,1 milhões seja utilizado
# em todas as execuções.
#
# Depois:
#
# 2.100.000 registros selecionados
#          ↓
# 80% treino / 20% teste
#          ↓
# Random Forest V2