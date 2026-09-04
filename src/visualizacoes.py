from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt

# Localiza a pasta raiz do projeto para permitir o acesso aos módulos do src.
ROOT = Path(__file__).resolve().parent.parent

# Adiciona a raiz ao caminho de execução do Python, caso ainda não esteja.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Importa a função responsável pela conexão com o PostgreSQL.
from src.database import get_connection

# Tabela tratada utilizada como fonte para as visualizações.
TABELA = "dw_enem.microdados_enem_tratado"


def consultar(sql):
    """Executa uma consulta SQL e retorna os dados em um DataFrame."""
    conn = get_connection()
    try:
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()

# 1. TAXA DE AUSÊNCIA POR ANO
# Objetivo:
# Visualizar a evolução da taxa de ausência na prova de Ciências da Natureza ao longo dos anos de 2019 a 2023.
# Principal output:
# percentual de participantes ausentes em cada ano.
# Essa visualização permite identificar mudanças no comportamento de ausência ao longo do período analisado e facilita a identificação de anos que apresentaram taxas significativamente maiores ou menores.

def grafico_taxa_ausencia_por_ano():
    """Gráfico da taxa de ausência em Ciências da Natureza por ano."""
    df = consultar(f"""
        SELECT "NU_ANO" AS ano,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "NU_ANO"
        ORDER BY "NU_ANO";
    """)
    plt.figure(figsize=(9, 5))
    plt.plot(df["ano"], df["taxa_ausencia"], marker="o")
    plt.title("Taxa de ausência no ENEM por ano - Ciências da Natureza")
    plt.xlabel("Ano")
    plt.ylabel("Taxa de ausência (%)")
    plt.xticks(df["ano"])
    plt.grid(True, alpha=0.3)
    for x, y in zip(df["ano"], df["taxa_ausencia"]):
        plt.annotate(f"{y:.2f}%", (x, y), textcoords="offset points", xytext=(0, 8), ha="center")
    plt.tight_layout()
    plt.show()


# 2. PRIMEIRO DIA X SEGUNDO DIA
# Objetivo:
# Comparar visualmente a taxa de ausência entre as provas do primeiro e do segundo dia do ENEM.
# CN representa Ciências da Natureza, realizada no primeiro dia.
# CH representa Ciências Humanas, realizada no segundo dia.
# Principal output:
# duas linhas com a taxa de ausência de CN e CH para cada ano.
# Essa comparação permite verificar se a ausência tende a ser maior em um dos
# dias de aplicação e se esse comportamento se mantém ao longo dos anos.

def grafico_primeiro_vs_segundo_dia():
    """Compara as taxas de ausência do primeiro e do segundo dia."""
    df = consultar(f"""
        SELECT "NU_ANO" AS ano,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia_cn,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CH" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia_ch
        FROM {TABELA}
        GROUP BY "NU_ANO"
        ORDER BY "NU_ANO";
    """)
    plt.figure(figsize=(9, 5))
    plt.plot(df["ano"], df["taxa_ausencia_cn"], marker="o", label="1º dia - CN")
    plt.plot(df["ano"], df["taxa_ausencia_ch"], marker="o", label="2º dia - CH")
    plt.title("Taxa de ausência: primeiro x segundo dia")
    plt.xlabel("Ano")
    plt.ylabel("Taxa de ausência (%)")
    plt.xticks(df["ano"])
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# 3. SEXO X AUSÊNCIA
# Objetivo:
# Visualizar a diferença na taxa de ausência entre os participantes classificados nas categorias de sexo disponíveis na base.
# Principal output:
# taxa de ausência para cada categoria de TP_SEXO.
# O gráfico facilita a comparação entre os grupos e permite observar se existe diferença relevante na ocorrência de ausência de acordo com o sexo.

def grafico_sexo():
    """Compara a taxa de ausência por sexo."""
    df = consultar(f"""
        SELECT "TP_SEXO" AS sexo,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "TP_SEXO"
        ORDER BY "TP_SEXO";
    """)
    plt.figure(figsize=(7, 5))
    barras = plt.bar(df["sexo"], df["taxa_ausencia"])
    plt.title("Taxa de ausência por sexo")
    plt.xlabel("Sexo")
    plt.ylabel("Taxa de ausência (%)")
    plt.ylim(0, max(df["taxa_ausencia"]) * 1.2)
    for barra, valor in zip(barras, df["taxa_ausencia"]):
        plt.text(barra.get_x() + barra.get_width() / 2, valor + 0.5, f"{valor:.2f}%", ha="center")
    plt.tight_layout()
    plt.show()


# 4. FAIXA ETÁRIA X AUSÊNCIA
# Objetivo:
# Visualizar como a taxa de ausência varia entre as diferentes faixas etárias dos participantes.
# Principal output:
# taxa de ausência para cada código de TP_FAIXA_ETARIA.
# Essa visualização permite identificar as faixas etárias com maiores e menores taxas de ausência e observar possíveis padrões relacionados à idade.

def grafico_faixa_etaria():
    """Mostra a taxa de ausência por faixa etária."""
    df = consultar(f"""
        SELECT "TP_FAIXA_ETARIA" AS faixa_etaria,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "TP_FAIXA_ETARIA"
        ORDER BY "TP_FAIXA_ETARIA";
    """)
    plt.figure(figsize=(11, 6))
    plt.bar(df["faixa_etaria"].astype(str), df["taxa_ausencia"])
    plt.title("Taxa de ausência por faixa etária")
    plt.xlabel("Código da faixa etária")
    plt.ylabel("Taxa de ausência (%)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


# 5. COR/RAÇA X AUSÊNCIA
# Objetivo:
# Visualizar a taxa de ausência de acordo com as categorias de cor/raça declaradas pelos participantes.
# Principal output:
# taxa de ausência para cada categoria de TP_COR_RACA.
# Essa análise permite comparar o comportamento de ausência entre os grupos de cor/raça presentes na base de dados.
# As categorias são apresentadas pelos códigos utilizados na base tratada.

def grafico_cor_raca():
    """Mostra a taxa de ausência por categoria de cor/raça."""
    df = consultar(f"""
        SELECT "TP_COR_RACA" AS cor_raca,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "TP_COR_RACA"
        ORDER BY "TP_COR_RACA";
    """)
    plt.figure(figsize=(8, 5))
    barras = plt.bar(df["cor_raca"].astype(str), df["taxa_ausencia"])
    plt.title("Taxa de ausência por cor/raça")
    plt.xlabel("Código de cor/raça")
    plt.ylabel("Taxa de ausência (%)")
    plt.ylim(0, max(df["taxa_ausencia"]) * 1.2)
    for barra, valor in zip(barras, df["taxa_ausencia"]):
        plt.text(barra.get_x() + barra.get_width() / 2, valor + 0.5, f"{valor:.2f}%", ha="center")
    plt.tight_layout()
    plt.show()


# 6. RENDA FAMILIAR X AUSÊNCIA
# Objetivo:
# Visualizar a relação entre a faixa de renda familiar declarada e a taxa de ausência dos participantes.
# Q006 representa a faixa de renda familiar informada no questionário socioeconômico.
# Principal output:
# taxa de ausência para cada categoria de Q006.
# As categorias sem informação são removidas da visualização para evitar que valores ausentes sejam interpretados como uma faixa de renda.
# O gráfico permite observar se a taxa de ausência apresenta diferenças conforme a faixa de renda familiar.

def grafico_renda():
    """Mostra a taxa de ausência por faixa de renda Q006."""
    df = consultar(f"""
        SELECT "Q006" AS faixa_renda,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "Q006"
        ORDER BY CASE WHEN TRIM("Q006") = '' THEN 999 ELSE ASCII(UPPER(TRIM("Q006"))) END;
    """)
    df = df[df["faixa_renda"].notna()]
    df = df[df["faixa_renda"].astype(str).str.strip() != ""]
    plt.figure(figsize=(11, 6))
    barras = plt.bar(df["faixa_renda"], df["taxa_ausencia"])
    plt.title("Taxa de ausência por faixa de renda familiar")
    plt.xlabel("Faixa de renda - Q006")
    plt.ylabel("Taxa de ausência (%)")
    plt.grid(axis="y", alpha=0.3)
    for barra, valor in zip(barras, df["taxa_ausencia"]):
        plt.text(barra.get_x() + barra.get_width() / 2, valor + 0.5, f"{valor:.1f}%", ha="center")
    plt.tight_layout()
    plt.show()


# 7. UF X AUSÊNCIA
# Objetivo:
# Visualizar as diferenças na taxa de ausência entre as Unidades da Federação.
# Principal output:
# taxa de ausência de cada UF, apresentada em ordem decrescente.
# A ordenação facilita a identificação dos estados com maiores e menores taxas de ausência.
# Essa visualização permite observar se o comportamento de ausência varia de acordo com a localização geográfica dos participantes.

def grafico_uf():
    """Mostra a taxa de ausência por estado."""
    df = consultar(f"""
        SELECT "SG_UF_PROVA" AS uf,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "SG_UF_PROVA"
        ORDER BY taxa_ausencia DESC;
    """)
    plt.figure(figsize=(11, 8))
    plt.barh(df["uf"], df["taxa_ausencia"])
    plt.gca().invert_yaxis()
    plt.title("Taxa de ausência por Unidade da Federação")
    plt.xlabel("Taxa de ausência (%)")
    plt.ylabel("UF")
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.show()


# 8. TIPO DE ESCOLA X AUSÊNCIA
# Objetivo:
# Visualizar a taxa de ausência de acordo com o tipo de escola informado pelos participantes.
# Principal output:
# taxa de ausência para cada categoria de TP_ESCOLA.
# O gráfico permite comparar os diferentes tipos de escola e identificar possíveis diferenças na ocorrência de ausência entre esses grupos.
# As categorias são apresentadas pelos códigos utilizados na base tratada.

def grafico_tipo_escola():
    """Mostra a taxa de ausência por tipo de escola."""
    df = consultar(f"""
        SELECT "TP_ESCOLA" AS tipo_escola,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "TP_ESCOLA"
        ORDER BY "TP_ESCOLA";
    """)
    plt.figure(figsize=(8, 5))
    barras = plt.bar(df["tipo_escola"].astype(str), df["taxa_ausencia"])
    plt.title("Taxa de ausência por tipo de escola")
    plt.xlabel("Código do tipo de escola")
    plt.ylabel("Taxa de ausência (%)")
    plt.ylim(0, max(df["taxa_ausencia"]) * 1.2)
    for barra, valor in zip(barras, df["taxa_ausencia"]):
        plt.text(barra.get_x() + barra.get_width() / 2, valor + 0.5, f"{valor:.2f}%", ha="center")
    plt.tight_layout()
    plt.show()


# EXECUÇÃO DAS VISUALIZAÇÕES
# Executa todas as visualizações desenvolvidas para a análise.
# Os gráficos são apresentados individualmente, permitindo analisar:
# - evolução da ausência ao longo dos anos;
# - diferença entre o primeiro e o segundo dia;
# - perfil por sexo;
# - perfil por faixa etária;
# - perfil por cor/raça;
# - perfil socioeconômico por renda;
# - diferenças entre as Unidades da Federação;
# - diferenças por tipo de escola.
# As visualizações complementam os resultados obtidos na Análise Exploratória.

def main():
    print("=" * 80)
    print("VISUALIZAÇÕES - ENEM: QUEM NÃO FOI?")
    print("=" * 80)
    print("Gerando os gráficos...")

    grafico_taxa_ausencia_por_ano()
    grafico_primeiro_vs_segundo_dia()
    grafico_sexo()
    grafico_faixa_etaria()
    grafico_cor_raca()
    grafico_renda()
    grafico_uf()
    grafico_tipo_escola()

    print("\nVisualizações concluídas com sucesso.")

if __name__ == "__main__":
    main()

# Rodei com  python .\src\visualizacoes.py 