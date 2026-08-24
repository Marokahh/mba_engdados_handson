from database import get_connection

def test_connection():
    try:
        connection = get_connection()

        print("Conexão com PostgreSQL realizada com sucesso!")

        connection.close()
        print("Conexão encerrada.")

    except Exception as error:
        print("Erro ao conectar com PostgreSQL:")
        print(error)


if __name__ == "__main__":
    test_connection()


# Rodei com o comando: & C:\Users\PAOLA\AppData\Local\Microsoft\WindowsApps\python3.11.exe mba_engdados_handson/src/test_connection.py