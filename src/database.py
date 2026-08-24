import psycopg2

from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def testar_conexao():
    try:
        conexao = get_connection()

        print("Conexão com PostgreSQL realizada com sucesso!")

        conexao.close()

        print("Conexão encerrada.")

    except Exception as erro:
        print("Erro ao conectar ao PostgreSQL:")
        print(erro)


if __name__ == "__main__":
    testar_conexao()