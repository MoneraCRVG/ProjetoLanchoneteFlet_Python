import mysql.connector

user = "root"
senha = ""
host = "localhost"
banco = "lanchonete_sabrina"


def conectar():
    conexao = None

    try:
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=senha,
            database=banco
        )
        if conexao.is_connected():
            print("Conexão estabelecida")

            cursor = conexao.cursor()

            cursor.execute("SHOW DATABASES")
            retorno = cursor.fetchall()

            print("Banco de dados", retorno)


    except mysql.connector.Error as e:
        print(f"Erro ao conectar com o BD: {e}")

    return conexao

def fechar_conexao(conexao):
    if conexao.is_connected():
        conexao.close()

conexao = conectar()

def inserir(conexao, descricao, valor, qtd):
    try:
        cursor = conexao.cursor()
        query = "INSERT INTO produto (descricao, preco, qtd) VALUES (%s, %s, %s)"

        cursor.execute(query, (descricao, valor, qtd))

        conexao.commit()

        print(f"{descricao} Registrado com sucesso")

    except mysql.connector.errors as e:
        print(f"Erro ao inserir produto: {e}")
    finally:
        cursor.close()

def delete(conexao, idProduto):
    try:
        cursor = conexao.cursor()
        query = "DELETE FROM products where id_codigo_produto=%s"

        cursor.execute(query, (idProduto))

        conexao.commit()
        print(f"{idProduto} Excluído!")

    except mysql.connector.Error as e:
        print(f"Erro ao excluir produto: {e}")

    finally:
        cursor.close()


def listar(conexao):
    try:
        cursor = conexao.cursor()
        query = "Select * from produto"
        cursor.execute(query)

        resultados = cursor.fetchall()

        for resultado in resultados:
            print(resultado)
    except mysql.connector.errors as e:
        print(f"Erro ao listar produtos: {e}")
    finally:
        cursor.close()
if conexao !=None:
    print("Conectado com o banco de dados")
    listar(conexao)
    fechar_conexao(conexao)