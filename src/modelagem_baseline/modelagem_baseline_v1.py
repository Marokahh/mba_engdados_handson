from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent

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

    # 0 = ausente
    # 1 = presente
    #
    # O baseline sempre irá prever a classe mais frequente.

    print("\nVariável alvo: TP_PRESENCA_CN")
    print("0 = Ausente")
    print("1 = Presente")

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
    # Exemplo:
    # Se a maior parte dos participantes estiver presente,
    # o modelo sempre irá responder "Presente".

    if ausentes > presentes:
        classe_baseline = 0
        nome_classe = "Ausente"
        proporcao = taxa_ausencia
    else:
        classe_baseline = 1
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

    # Como o baseline sempre prevê uma única classe:
    #
    # Accuracy = proporção da classe majoritária
    # Precision = proporção de acertos entre as previsões positivas
    # Recall = proporção de positivos corretamente identificados
    # F1 = equilíbrio entre Precision e Recall
    #
    # Para facilitar a comparação posterior, calculamos
    # também a matriz de confusão.

    if classe_baseline == 1:

        verdadeiro_positivo = presentes
        falso_positivo = ausentes
        falso_negativo = 0
        verdadeiro_negativo = 0

    else:

        verdadeiro_positivo = ausentes
        falso_positivo = presentes
        falso_negativo = 0
        verdadeiro_negativo = 0

    accuracy = (verdadeiro_positivo + verdadeiro_negativo) / total

    precision = (
        verdadeiro_positivo /
        (verdadeiro_positivo + falso_positivo)
    )

    recall = (
        verdadeiro_positivo /
        (verdadeiro_positivo + falso_negativo)
    )

    f1 = (
        2 * precision * recall /
        (precision + recall)
    )

    # Balanced Accuracy
    #
    # Como o baseline prevê apenas uma classe,
    # a especificidade da classe não prevista é 0.

    especificidade = 0

    balanced_accuracy = (recall + especificidade) / 2

    print("\n" + "-" * 80)
    print("MÉTRICAS DO BASELINE")
    print("-" * 80)

    print(f"Accuracy          : {accuracy:.4f} ({accuracy:.2%})")
    print(f"Precision         : {precision:.4f}")
    print(f"Recall            : {recall:.4f}")
    print(f"F1-score          : {f1:.4f}")
    print(f"Balanced Accuracy : {balanced_accuracy:.4f}")

    # ============================================================
    # 5. MATRIZ DE CONFUSÃO
    # ============================================================

    print("\n" + "-" * 80)
    print("MATRIZ DE CONFUSÃO")
    print("-" * 80)

    print("""
                    PREVISTO
                 Ausente  Presente
REAL  Ausente       ...       ...
      Presente      ...       ...
    """)

    if classe_baseline == 1:
        print(f"Ausente  ->  0        {ausentes:,}")
        print(f"Presente ->  0        {presentes:,}")
    else:
        print(f"Ausente  ->  {ausentes:,}        0")
        print(f"Presente ->  {presentes:,}        0")

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
        f"Com essa estratégia, o modelo apresenta "
        f"Accuracy de {accuracy:.2%}."
    )

    print(
        "\nEssas métricas serão utilizadas como referência "
        "para comparar os modelos de Machine Learning."
    )

    print(
        "\nUm modelo posterior deverá superar esse resultado "
        "para demonstrar que está aprendendo padrões dos dados "
        "e não apenas reproduzindo a classe mais frequente."
    )

    cursor.close()
    conn.close()

    print("\nBaseline concluído com sucesso.")


if __name__ == "__main__":
    main()


# Rodei no run

# O que esse primeiro modelo faz? Modelo orientado à classe Presente
# V1: avaliação inicialmente estruturada com Presente como classe positiva.
# Então ele não usa idade, renda, UF, escola etc. Ainda não é o Machine Learning de verdade. É a nossa referência.
# As métricas que vamos guardar para a próxima etapa são: Accuracy, Precision, Recall, F1-score, Balanced Accuracy, Matriz de confusão
# E depois vamos fazer algo importante: Random Forest e XGBoost terão que ser avaliados com as mesmas métricas, para conseguirmos justificar no trabalho qual modelo teve melhor desempenho.