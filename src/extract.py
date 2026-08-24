import os

import pandas as pd
import psycopg2
from psycopg2 import sql

from config import DB_CONFIG, DATA_DIR, SCHEMA_STAGING, ANOS


def encontrar_arquivo(ano):
    """
    Localiza o CSV correspondente ao ano.
    """

    arquivo = os.path.join(
        DATA_DIR,
        f"MICRODADOS_ENEM_{ano}.csv"
    )

    if not os.path.exists(arquivo):
        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo}"
        )

    return arquivo


def analisar_csv(arquivo, ano):
    """
    Usa Pandas para ler apenas uma pequena amostra
    do arquivo e apresentar informações no terminal.
    """

    print("\n" + "-" * 70)
    print(f"ANÁLISE DO ARQUIVO {ano}")
    print("-" * 70)

    print(f"Arquivo: {arquivo}")

    # Lê somente o cabeçalho
    df_colunas = pd.read_csv(
        arquivo,
        sep=";",
        encoding="latin-1",
        nrows=0,
        dtype=str
    )

    colunas = list(df_colunas.columns)

    print(f"\nQuantidade de colunas: {len(colunas)}")

    print("\nColunas:")

    for numero, coluna in enumerate(colunas, start=1):
        print(f"{numero:03d} - {coluna}")

    # Lê somente 5 registros para visualização
    df_amostra = pd.read_csv(
        arquivo,
        sep=";",
        encoding="latin-1",
        nrows=5,
        dtype=str,
        keep_default_na=False
    )

    print("\nPrimeiras 5 linhas:")

    print(df_amostra.to_string(index=False))

    print("\nTipos identificados pelo Pandas:")

    print(df_amostra.dtypes)

    return colunas


def criar_tabela(cursor, ano, colunas):
    """
    Cria a tabela de staging usando todas as colunas
    como TEXT, preservando os dados brutos.
    """

    nome_tabela = f"microdados_enem_{ano}"

    print(
        f"\nCriando tabela "
        f"{SCHEMA_STAGING}.{nome_tabela}..."
    )

    # Garante que o schema exista
    cursor.execute(
        sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
            sql.Identifier(SCHEMA_STAGING)
        )
    )

    # Se a tabela já existir, remove para permitir
    # uma nova carga limpa.
    cursor.execute(
        sql.SQL("DROP TABLE IF EXISTS {}.{}").format(
            sql.Identifier(SCHEMA_STAGING),
            sql.Identifier(nome_tabela)
        )
    )

    definicoes_colunas = []

    for coluna in colunas:

        definicoes_colunas.append(
            sql.SQL("{} TEXT").format(
                sql.Identifier(coluna)
            )
        )

    comando = sql.SQL("""
        CREATE TABLE {}.{} (
            {}
        )
    """).format(
        sql.Identifier(SCHEMA_STAGING),
        sql.Identifier(nome_tabela),
        sql.SQL(", ").join(definicoes_colunas)
    )

    cursor.execute(comando)

    print("Tabela criada com sucesso.")

    return nome_tabela


def carregar_csv(cursor, arquivo, tabela):
    """
    Carrega o CSV diretamente para o PostgreSQL
    utilizando COPY.
    """

    print("\nIniciando carga para o PostgreSQL...")
    print("Aguarde. Arquivos do ENEM são grandes.")

    comando_copy = sql.SQL("""
        COPY {}.{}
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE,
            DELIMITER ';',
            QUOTE '"',
            ESCAPE '"',
            ENCODING 'LATIN1'
        )
    """).format(
        sql.Identifier(SCHEMA_STAGING),
        sql.Identifier(tabela)
    )

    with open(arquivo, "rb") as arquivo_csv:

        cursor.copy_expert(
            comando_copy.as_string(cursor.connection),
            arquivo_csv
        )

    print("Carga concluída com sucesso!")


def verificar_carga(cursor, tabela):
    """
    Consulta a quantidade de registros carregados.
    """

    cursor.execute(
        sql.SQL("""
            SELECT COUNT(*)
            FROM {}.{}
        """).format(
            sql.Identifier(SCHEMA_STAGING),
            sql.Identifier(tabela)
        )
    )

    quantidade = cursor.fetchone()[0]

    print(
        f"Quantidade de registros no banco: "
        f"{quantidade:,}"
    )

    return quantidade


def extrair_ano(ano):
    """
    Executa a extração completa de um ano.
    """

    print("\n")
    print("=" * 70)
    print(f"INICIANDO EXTRAÇÃO ENEM {ano}")
    print("=" * 70)

    arquivo = encontrar_arquivo(ano)

    print(f"\nArquivo encontrado:")
    print(arquivo)

    # Pandas apenas para análise/visualização
    colunas = analisar_csv(
        arquivo,
        ano
    )

    conexao = psycopg2.connect(**DB_CONFIG)

    try:

        cursor = conexao.cursor()

        tabela = criar_tabela(
            cursor,
            ano,
            colunas
        )

        conexao.commit()

        carregar_csv(
            cursor,
            arquivo,
            tabela
        )

        conexao.commit()

        quantidade = verificar_carga(
            cursor,
            tabela
        )

        conexao.commit()

        cursor.close()

    except Exception:

        conexao.rollback()

        raise

    finally:

        conexao.close()

    print("\n" + "=" * 70)
    print(f"EXTRAÇÃO {ano} FINALIZADA")
    print(
        f"Tabela: {SCHEMA_STAGING}.{tabela}"
    )
    print(
        f"Registros carregados: {quantidade:,}"
    )
    print("=" * 70)


def main():

    print("\n")
    print("#" * 70)
    print("# ETL ENEM - ETAPA DE EXTRAÇÃO")
    print("#" * 70)

    print("\nAnos que serão processados:")

    for ano in ANOS:
        print(f"- {ano}")

    for ano in ANOS:

        try:

            extrair_ano(ano)

        except Exception as erro:

            print("\n" + "!" * 70)
            print(f"ERRO NA EXTRAÇÃO DO ANO {ano}")
            print("!" * 70)

            print(f"\nErro:")
            print(erro)

            print(
                "\nA execução foi interrompida "
                f"no ano {ano}."
            )

            break

    print("\n")
    print("#" * 70)
    print("# PROCESSO FINALIZADO")
    print("#" * 70)


if __name__ == "__main__":
    main()

# Para rodar dentro da pasta do projeto: python src/extract.py