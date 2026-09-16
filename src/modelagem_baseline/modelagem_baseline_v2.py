from pathlib import Path
import sys

# Localiza a raiz do projeto
ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.database import get_connection


TABELA = "dw_enem.microdados_enem_tratado"


def main():

    conn = get_connection()
    cursor = conn.cursor()

    print("\n" + "=" * 80)
    print("MODELO BASELINE - PREVISÃO DE AUSÊNCIA NO ENEM")
    print("=" * 80)

    # ============================================================
    # 1. DEFINIÇÃO DA VARIÁVEL ALVO
    # ============================================================

    # No banco:
    # TP_PRESENCA_CN = 0 -> Ausente
    # TP_PRESENCA_CN = 1 -> Presente
    #
    # Para o modelo:
    # 0 = Presente
    # 1 = Ausente

    print("\nVariável alvo: TP_PRESENCA_CN")
    print("0 = Presente")
    print("1 = Ausente")

    # ============================================================
    # 2. CONTAGEM DAS CLASSES
    # ============================================================

    cursor.execute(f"""
        SELECT
            COUNT(*) FILTER (
                WHERE "TP_PRESENCA_CN" = 0
            ) AS ausentes,

            COUNT(*) FILTER (
                WHERE "TP_PRESENCA_CN" = 1
            ) AS presentes

        FROM {TABELA};
    """)

    ausentes, presentes = cursor.fetchone()

    total = ausentes + presentes

    print("\n" + "-" * 80)
    print("DISTRIBUIÇÃO DA VARIÁVEL ALVO")
    print("-" * 80)

    print(f"Ausentes : {ausentes:,}")
    print(f"Presentes: {presentes:,}")
    print(f"Total    : {total:,}")

    taxa_ausencia = ausentes / total
    taxa_presenca = presentes / total

    print(f"\nTaxa de ausência : {taxa_ausencia:.2%}")
    print(f"Taxa de presença : {taxa_presenca:.2%}")

    # ============================================================
    # 3. DEFINIÇÃO DO BASELINE
    # ============================================================

    # O baseline sempre prevê a classe mais frequente.
    #
    # Neste caso, Presente é a classe majoritária.
    # Portanto, o baseline sempre prevê:
    #
    # 0 = Presente

    if ausentes > presentes:

        classe_baseline = 1
        nome_classe = "Ausente"
        proporcao = taxa_ausencia

    else:

        classe_baseline = 0
        nome_classe = "Presente"
        proporcao = taxa_presenca

    print("\n" + "-" * 80)
    print("BASELINE")
    print("-" * 80)

    print(f"Regra: sempre prever '{nome_classe}'")
    print(f"Classe prevista: {classe_baseline}")

    # ============================================================
    # 4. MÉTRICAS
    # ============================================================

    # Estamos avaliando a classe AUSENTE = 1.
    #
    # Como o baseline sempre prevê Presente (0):
    #
    # Verdadeiro Positivo (VP) = 0
    # Falso Positivo (FP) = 0
    # Falso Negativo (FN) = todos os ausentes
    # Verdadeiro Negativo (VN) = todos os presentes

    if classe_baseline == 0:

        verdadeiro_positivo = 0
        falso_positivo = 0
        falso_negativo = ausentes
        verdadeiro_negativo = presentes

    else:

        verdadeiro_positivo = ausentes
        falso_positivo = presentes
        falso_negativo = 0
        verdadeiro_negativo = 0

    # Accuracy
    accuracy = (
        verdadeiro_positivo + verdadeiro_negativo
    ) / total

    # Precision
    if verdadeiro_positivo + falso_positivo > 0:

        precision = (
            verdadeiro_positivo /
            (verdadeiro_positivo + falso_positivo)
        )

    else:

        precision = 0

    # Recall
    if verdadeiro_positivo + falso_negativo > 0:

        recall = (
            verdadeiro_positivo /
            (verdadeiro_positivo + falso_negativo)
        )

    else:

        recall = 0

    # F1-score
    if precision + recall > 0:

        f1 = (
            2 * precision * recall /
            (precision + recall)
        )

    else:

        f1 = 0

    # Recall da classe Ausente = Sensibilidade
    sensibilidade_ausente = recall

    # Especificidade
    # Capacidade de identificar corretamente os presentes.
    if verdadeiro_negativo + falso_positivo > 0:

        especificidade = (
            verdadeiro_negativo /
            (verdadeiro_negativo + falso_positivo)
        )

    else:

        especificidade = 0

    # Balanced Accuracy
    balanced_accuracy = (
        sensibilidade_ausente + especificidade
    ) / 2

    print("\n" + "-" * 80)
    print("MÉTRICAS DO BASELINE")
    print("-" * 80)

    print(f"Accuracy          : {accuracy:.4f} ({accuracy:.2%})")
    print(f"Precision (Ausente): {precision:.4f}")
    print(f"Recall (Ausente)   : {recall:.4f}")
    print(f"F1-score (Ausente) : {f1:.4f}")
    print(f"Especificidade     : {especificidade:.4f}")
    print(f"Balanced Accuracy  : {balanced_accuracy:.4f}")

    # ============================================================
    # 5. MATRIZ DE CONFUSÃO
    # ============================================================

    print("\n" + "-" * 80)
    print("MATRIZ DE CONFUSÃO")
    print("-" * 80)

    print("\n                    PREVISTO")
    print("                 Presente  Ausente")

    print(
        f"REAL Presente   {verdadeiro_negativo:,}        "
        f"{falso_positivo:,}"
    )

    print(
        f"     Ausente    {falso_negativo:,}        "
        f"{verdadeiro_positivo:,}"
    )

    # ============================================================
    # 6. CONCLUSÃO
    # ============================================================

    print("\n" + "=" * 80)
    print("CONCLUSÃO DO BASELINE")
    print("=" * 80)

    print(
        f"\nO modelo baseline sempre prevê '{nome_classe}'."
    )

    print(
        f"Accuracy: {accuracy:.2%}"
    )

    print(
        f"Recall para Ausente: {recall:.2%}"
    )

    print(
        f"F1-score para Ausente: {f1:.2%}"
    )

    print(
        "\nO baseline será utilizado como referência "
        "para avaliar os modelos de Machine Learning."
    )

    print(
        "Os próximos modelos deverão apresentar desempenho "
        "superior principalmente na identificação dos ausentes."
    )

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()


# Rodei no run

# O que esse segundo modelo faz? Modelo orientado à identificação dos Ausentes
# V2: avaliação ajustada para Ausente = 1, tornando as métricas de Precision, Recall e F1-score diretamente relacionadas ao objetivo do projeto: identificar participantes ausentes.
# Importante: a V2 não mudou a regra do baseline nem os dados. Mudamos a interpretação da variável alvo para que a avaliação esteja alinhada ao problema que queremos resolver.