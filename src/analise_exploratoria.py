from pathlib import Path
import sys

# Localiza a pasta raiz do projeto para permitir o acesso aos módulos do src.
ROOT = Path(__file__).resolve().parent.parent

# Adiciona a raiz ao caminho de execução do Python, caso ainda não esteja.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Importa a função responsável pela conexão com o PostgreSQL.
from src.database import get_connection

# Tabela tratada utilizada como fonte para a Análise Exploratória.
TABELA = "dw_enem.microdados_enem_tratado"


def executar(cursor, titulo, sql):
    print("\n" + "=" * 80)
    print(titulo)
    print("=" * 80)
    cursor.execute(sql)
    colunas = [d[0] for d in cursor.description]
    rows = cursor.fetchall()

    if not rows:
        print("Nenhum resultado encontrado.")
        return rows

    larguras = []
    for i, coluna in enumerate(colunas):
        maior = len(str(coluna))
        if rows:
            maior = max(maior, max(len(str(row[i])) for row in rows))
        larguras.append(maior)

    print(" | ".join(str(colunas[i]).ljust(larguras[i]) for i in range(len(colunas))))
    print("-+-".join("-" * w for w in larguras))
    for row in rows:
        print(" | ".join(str(row[i]).ljust(larguras[i]) for i in range(len(colunas))))
    return rows

# Conexão com o Banco de Dados
# Abre a conexão com o PostgreSQL e cria um cursor para executar as consultas SQL.
def main():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. PRESENÇA E AUSÊNCIA POR ANO
    # Objetivo:
    # Identificar como a presença dos participantes na prova de Ciências
    # da Natureza (CN) se distribui entre 2019 e 2023.
    #
    # Código de presença:
    # 0 = ausente
    # 1 = presente
    # 2 = eliminado
    #
    # Além da quantidade de participantes, calculamos o percentual de cada
    # situação dentro de cada ano.
    #
    # Principal output:
    # quantidade e percentual de ausentes, presentes e eliminados por ano.

    executar(cursor, "1. PRESENCA E AUSENCIA POR ANO - CN", f'''
        SELECT "NU_ANO", "TP_PRESENCA_CN", COUNT(*) AS quantidade,
               ROUND(COUNT(*) * 100.0 /
               SUM(COUNT(*)) OVER (PARTITION BY "NU_ANO"), 2) AS percentual
        FROM {TABELA}
        GROUP BY "NU_ANO", "TP_PRESENCA_CN"
        ORDER BY "NU_ANO", "TP_PRESENCA_CN";
    ''')

    # 2. TAXA DE AUSÊNCIA POR ANO
    # Objetivo:
    # Medir a taxa de ausência na prova de Ciências da Natureza em cada ano.
    #
    # Aqui transformamos a quantidade absoluta de ausentes em uma taxa
    # percentual, permitindo comparar os anos mesmo com diferentes números
    # de participantes.
    #
    # Principal output:
    # ano, quantidade de ausentes, presentes, total de participantes e
    # taxa de ausência.
    #
    # Essa análise permite identificar anos com aumento ou redução da
    # ausência e possíveis mudanças de comportamento ao longo do período.

    taxa = executar(cursor, "2. TAXA DE AUSENCIA POR ANO - CN", f'''
        SELECT "NU_ANO" AS ano,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) AS ausentes,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 1) AS presentes,
               COUNT(*) AS total,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "NU_ANO"
        ORDER BY "NU_ANO";
    ''')

    # 3. COMPARAÇÃO ENTRE O PRIMEIRO E O SEGUNDO DIA
    # Objetivo:
    # Verificar se o comportamento de ausência muda entre os dias de aplicação do ENEM.
    #
    # CN representa Ciências da Natureza e ocorre no primeiro dia.
    # CH representa Ciências Humanas e ocorre no segundo dia.
    #
    # Principal output:
    # taxa de ausência em CN, taxa de ausência em CH e diferença entre elas em pontos percentuais para cada ano.
    # Essa comparação ajuda a identificar se existe maior abandono/ausência em um dos dias de aplicação.

    executar(cursor, "3. TAXA DE AUSENCIA - PRIMEIRO X SEGUNDO DIA", f'''
        SELECT "NU_ANO" AS ano,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia_cn,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CH" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia_ch,
               ROUND(
                   COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*)
                   - COUNT(*) FILTER (WHERE "TP_PRESENCA_CH" = 0) * 100.0 / COUNT(*), 2
               ) AS diferenca_pontos_percentuais
        FROM {TABELA}
        GROUP BY "NU_ANO"
        ORDER BY "NU_ANO";
    ''')

    # 4. PERFIL DEMOGRÁFICO — SEXO
    # Objetivo:
    # Investigar se a taxa de ausência apresenta diferenças entre os sexos.
    #
    # Principal output:
    # total de participantes, ausentes, presentes e taxa de ausência para cada categoria de TP_SEXO.
    # Essa análise permite comparar o comportamento de ausência entre os grupos, considerando a proporção de ausentes dentro de cada grupo.

    sexo = executar(cursor, "4. PERFIL DEMOGRAFICO - SEXO X AUSENCIA", f'''
        SELECT "TP_SEXO" AS sexo, COUNT(*) AS total,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) AS ausentes,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 1) AS presentes,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "TP_SEXO"
        ORDER BY "TP_SEXO";
    ''')

    # 5. PERFIL DEMOGRÁFICO — FAIXA ETÁRIA
    # Objetivo:
    # Investigar a relação entre idade/faixa etária e ausência na prova.
    #
    # Principal output:
    # total de participantes, ausentes, presentes e taxa de ausência por faixa etária.
    # Essa análise permite identificar faixas etárias com maior ou menor concentração proporcional de ausentes.

    idade = executar(cursor, "5. PERFIL DEMOGRAFICO - FAIXA ETARIA X AUSENCIA", f'''
        SELECT "TP_FAIXA_ETARIA" AS faixa_etaria, COUNT(*) AS total,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) AS ausentes,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 1) AS presentes,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "TP_FAIXA_ETARIA"
        ORDER BY "TP_FAIXA_ETARIA";
    ''')

    # 6. PERFIL SOCIOECONÔMICO — RENDA FAMILIAR
    # Q006 representa a faixa de renda familiar declarada pelo participante.
    #
    # Objetivo:
    # Investigar se existe relação entre a faixa de renda familiar e a ocorrência de ausência na prova.
    #
    # Principal output:
    # total de participantes, ausentes, presentes e taxa de ausência para cada categoria de Q006.
    # Essa análise é importante para verificar se a condição socioeconômica apresenta associação com o comportamento de ausência.

    renda = executar(cursor, "6. PERFIL SOCIOECONOMICO - Q006 X AUSENCIA", f'''
        SELECT "Q006" AS faixa_renda, COUNT(*) AS total,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) AS ausentes,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 1) AS presentes,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "Q006"
        ORDER BY CASE WHEN TRIM("Q006") = '' THEN 999 ELSE ASCII(UPPER(TRIM("Q006"))) END;
    ''')

    # 7. PERFIL GEOGRÁFICO — UF
    # Objetivo:
    # Identificar diferenças na taxa de ausência entre os estados brasileiros.
    #
    # Principal output:
    # total de participantes, ausentes, presentes e taxa de ausência por UF.
    # O resultado é ordenado pela taxa de ausência, permitindo identificar rapidamente os estados com maiores e menores taxas.

    uf = executar(cursor, "7. GEOGRAFIA - UF X AUSENCIA", f'''
        SELECT "SG_UF_PROVA" AS uf, COUNT(*) AS total,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) AS ausentes,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 1) AS presentes,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "SG_UF_PROVA"
        ORDER BY taxa_ausencia DESC;
    ''')

    # 8. PERFIL ESCOLAR — TIPO DE ESCOLA
    # Objetivo:
    # Investigar se a taxa de ausência varia de acordo com o tipo de escola informado pelo participante.
    #
    # Principal output:
    # total de participantes, ausentes, presentes e taxa de ausência por categoria de TP_ESCOLA.
    # Essa análise permite comparar o comportamento de ausência entre os diferentes tipos de escola.

    escola = executar(cursor, "8. PERFIL ESCOLAR - TP_ESCOLA X AUSENCIA", f'''
        SELECT "TP_ESCOLA" AS tipo_escola, COUNT(*) AS total,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) AS ausentes,
               COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 1) AS presentes,
               ROUND(COUNT(*) FILTER (WHERE "TP_PRESENCA_CN" = 0) * 100.0 / COUNT(*), 2) AS taxa_ausencia
        FROM {TABELA}
        GROUP BY "TP_ESCOLA"
        ORDER BY "TP_ESCOLA";
    ''')

    # 9. RESUMO DOS PRINCIPAIS ACHADOS
    # Esta seção não realiza uma nova consulta.
    #
    # Ela utiliza os resultados das análises anteriores para destacar automaticamente os maiores e menores valores encontrados.
    #
    # Principal output:
    # - ano com maior e menor taxa de ausência;
    # - sexo com maior e menor taxa;
    # - faixa etária com maior e menor taxa;
    # - faixa de renda com maior e menor taxa;
    # - UF com maior e menor taxa;
    # - tipo de escola com maior e menor taxa.
    # Esses resultados servem como ponto de partida para as interpretações da Análise Exploratória e para a criação das visualizações.

    print("\n" + "=" * 80)
    print("9. RESUMO DOS PRINCIPAIS ACHADOS")
    print("=" * 80)

    # Identifica o ano com maior e menor taxa de ausência.
    if taxa:
        maior = max(taxa, key=lambda x: float(x[4]))
        menor = min(taxa, key=lambda x: float(x[4]))
        print(f"- Maior taxa de ausencia: {maior[0]} ({maior[4]}%).")
        print(f"- Menor taxa de ausencia: {menor[0]} ({menor[4]}%).")

    # Identifica o sexo com maior e menor taxa de ausência.
    if sexo:
        print(f"- Sexo com menor taxa de ausencia: {min(sexo, key=lambda x: float(x[4]))[0]}")
        print(f"- Sexo com maior taxa de ausencia: {max(sexo, key=lambda x: float(x[4]))[0]}")

    # Identifica as faixas etárias com maior e menor taxa de ausência.
    if idade:
        maior = max(idade, key=lambda x: float(x[4]))
        menor = min(idade, key=lambda x: float(x[4]))
        print(f"- Faixa etaria com maior taxa: {maior[0]} ({maior[4]}%).")
        print(f"- Faixa etaria com menor taxa: {menor[0]} ({menor[4]}%).")

    # Remove a categoria vazia de Q006 antes de identificar os extremos.
    validas = [r for r in renda if str(r[0]).strip()]
    if validas:
        maior = max(validas, key=lambda x: float(x[4]))
        menor = min(validas, key=lambda x: float(x[4]))
        print(f"- Q006 com maior taxa: {maior[0]} ({maior[4]}%).")
        print(f"- Q006 com menor taxa: {menor[0]} ({menor[4]}%).")

    # Como a consulta de UF já está ordenada pela taxa de ausência, a primeira linha representa a maior taxa e a última a menor.
    if uf:
        print(f"- UF com maior taxa: {uf[0][0]} ({uf[0][4]}%).")
        print(f"- UF com menor taxa: {uf[-1][0]} ({uf[-1][4]}%).")

    # Identifica o tipo de escola com maior e menor taxa de ausência.
    if escola:
        maior = max(escola, key=lambda x: float(x[4]))
        menor = min(escola, key=lambda x: float(x[4]))
        print(f"- Tipo de escola com maior taxa: {maior[0]} ({maior[4]}%).")
        print(f"- Tipo de escola com menor taxa: {menor[0]} ({menor[4]}%).")

    # Encerra o cursor e a conexão com o banco.
    cursor.close()
    conn.close()
    print("\nAnalise exploratoria concluida com sucesso.")

# Executa a análise somente quando este arquivo for executado diretamente.
if __name__ == "__main__":
    main()

# Rodei com cd C:\Users\PAOLA\Downloads\ProjetoMBA_QuemNaoFoi\mba_engdados_handson
# python src/analise_exploratoria.py
