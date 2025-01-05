import mysql.connector # Importa o conector mysql-connector-python
import random # Importa a biblioteca para gerar números aleatórios

# Define a configuração para conexão
dbconfig = {
    "database": "lanchonete_sabrina",
    "user": "nicolas",
    "password": "senac",
    "host": "localhost"
}

# Cria um pool para ser usado em diferentes partes do sistema de forma eficiente
pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="lanchonete_sabrina", # Nome do pool
    pool_size=3, # Número máximo de conexões simultâneas
    **dbconfig # Passa as configurações como parâmetros dessa função
)
#region Produtos
# Função UPDATE para alterar um produto no banco de dados
def editar_produto(codigo, descricao, preco, quantidadeEstoque):
    query = """
    UPDATE produtos
    SET descricao = %s, preco = %s, quantidadeEstoque = %s
    WHERE codigo = %s
    """
    try:
        # Solicita conexão do pool
        cnx = pool.get_connection()
        # Inicializa o cursor
        cursor = cnx.cursor()
        # Executa a transação
        cursor.execute(query, (descricao, preco, quantidadeEstoque, codigo))
        # Salva (commit) as alterações no banco de dados
        cnx.commit()
    except mysql.connector.Error as e:
        # Se houver erro, desfaz a transação
        cnx.rollback()
        print(f"Erro: {e}")
    finally:
        # Encerra o cursor
        cursor.close()
        # Devolve a conexão para o pool
        cnx.close()

# Função INSERT para inserir um produto no banco de dados.
def enviar_produtos(descricao, preco, quantidadeEstoque):
    codigo = random.randint(0, 99999)
    query = """
        INSERT INTO produtos (codigo, descricao, preco, quantidadeEstoque)
        VALUES (%s, %s, %s, %s)
    """
    try:
        # Solicita conexão do pool
        cnx = pool.get_connection()
        # Inicializa o cursor
        cursor = cnx.cursor()
        print(descricao, preco, quantidadeEstoque)
        # Executa a transação
        cursor.execute(query, (codigo, descricao, preco, quantidadeEstoque))
        # Salva (commit) as alterações no banco de dados
        cnx.commit()
    except mysql.connector.Error as e:
        # Se houver erro, desfaz a transação
        cnx.rollback()
        print(f"Erro: {e}")
    finally:
        # Encerra o cursor
        cursor.close()
        # Devolve a conexão para o pool
        cnx.close()

# Função READ para listar todos os produtos no banco de dados
def listar_produtos():
    # Faz com que a variável result declarada no escopo 'try' seja visível nesse escopo.
    global result
    query = """SELECT * FROM produtos"""

    try:
        # Solicita conexão do pool
        cnx = pool.get_connection()
        # Inicializa o cursor
        cursor = cnx.cursor()
        # Executa a consulta.
        cursor.execute(query)
        # Extrai todos os resultados como uma lista de tuplas.
        result = cursor.fetchall()
        # Como é uma consulta de leitura (read-only), não precisa salvar a operação.
        print(result)
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        # Encerra o cursor
        cursor.close()
        # Devolve a conexão para o pool
        cnx.close()
        # Retorna os resultados da consulta
        return result

# Função READ para buscar um produto específico no banco de dados pelo código
def buscar_produto(codigo):
    # Faz com que a variável result declarada no escopo 'try' seja visível nesse escopo.
    global result
    # Variável de consulta
    query = """SELECT * FROM produtos WHERE codigo = %s"""
    try:
        # Solicita conexão do pool
        cnx = pool.get_connection()
        # Inicializa o cursor
        cursor = cnx.cursor()
        # Executa a consulta
        cursor.execute(query, (codigo,))
        # Extrai apenas o primeiro e único resultado da consulta. Isso é importante, pois retorna uma tupla única, e não uma lista de tuplas.
        result = cursor.fetchone()
        # Como é uma consulta de leitura (read-only), não precisa salvar a operação.
        print(result)
    except mysql.connector.Error as e:
        # Como é uma consulta de leitura (read-only), não precisa desfazer a transação em caso de erro.
        print(f"Erro: {e}")
        result = None
    finally:
        # Encerra o cursor
        cursor.close()
        # Devolve a conexão para o pool
        cnx.close()
        # Retorna os resultados da consulta
        return result

# Função DELETE para remover um produto no banco de dados
def deletar_produto(codigo):
    query = """DELETE FROM produtos WHERE codigo = %s"""
    try:
        # Solicita uma conexão ao pool
        cnx = pool.get_connection()
        # Cria um cursor
        cursor = cnx.cursor()
        # Executa o código SQL. Importante que para dados do usuário, esse tipo de método é importante pois evita ataques de SQL Injection.
        cursor.execute(query, (codigo,))
        # Salva (commit) as alterações no banco de dados
        cnx.commit()
        print(f"Produto {codigo} excluído com sucesso.")
    except mysql.connector.Error as e:
        # Se houver erro, desfaz a transação
        cnx.rollback()
        print(f"Erro: {e}")
    finally:
        # Encerra o cursor
        cursor.close()
        # Devolve a conexão para o pool
        cnx.close()
#endregion
#region Clientes
# Função UPDATE para alterar um cliente no banco de dados
def editar_cliente(codigo, cpf, nome, telefone, endereco):
    query = """
    UPDATE clientes
    SET  cpf = %s, nome = %s, telefone = %s, endereco = %s
    WHERE codigo = %s
    """
    try:
        # Solicita conexão do pool
        cnx = pool.get_connection()
        # Inicializa o cursor
        cursor = cnx.cursor()
        # Executa a transação
        cursor.execute(query, (cpf, nome, telefone, endereco, codigo))
        # Salva (commit) as alterações no banco de dados
        cnx.commit()
    except mysql.connector.Error as e:
        # Se houver erro, desfaz a transação
        cnx.rollback()
        print(f"Erro: {e}")
    finally:
        # Encerra o cursor
        cursor.close()
        # Devolve a conexão para o pool
        cnx.close()

# Função INSERT para inserir um cliente no banco de dados.
def enviar_clientes(cpf, nome, telefone, endereco):
    codigo = random.randint(0, 99999)
    query = """
        INSERT INTO clientes (codigo, cpf, nome, telefone, endereco)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        # Solicita conexão do pool
        cnx = pool.get_connection()
        # Inicializa o cursor
        cursor = cnx.cursor()
        print(cpf, nome, telefone, endereco)
        # Executa a transação
        cursor.execute(query, (codigo, cpf, nome, telefone, endereco))
        # Salva (commit) as alterações no banco de dados
        cnx.commit()
    except mysql.connector.Error as e:
        # Se houver erro, desfaz a transação
        cnx.rollback()
        print(f"Erro: {e}")
    finally:
        # Encerra o cursor
        cursor.close()
        # Devolve a conexão para o pool
        cnx.close()

# Função READ para listar todos os clientes no banco de dados
def listar_clientes():
    # Faz com que a variável result declarada no escopo 'try' seja visível nesse escopo.
    global results
    query = """SELECT * FROM clientes"""

    try:
        # Solicita conexão do pool
        cnx = pool.get_connection()
        # Inicializa o cursor
        cursor = cnx.cursor()
        # Executa a consulta.
        cursor.execute(query)
        # Extrai todos os resultados como uma lista de tuplas.
        results = cursor.fetchall()
        # Como é uma consulta de leitura (read-only), não precisa salvar a operação.
        print(results)
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        # Encerra o cursor
        cursor.close()
        # Devolve a conexão para o pool
        cnx.close()
        # Retorna os resultados da consulta
        return results

# Função READ para buscar um cliente específico no banco de dados pelo código
def buscar_cliente(codigo):
    # Faz com que a variável result declarada no escopo 'try' seja visível nesse escopo.
    global result
    # Variável de consulta
    query = """SELECT * FROM clientes WHERE codigo = %s"""
    try:
        # Solicita conexão do pool
        cnx = pool.get_connection()
        # Inicializa o cursor
        cursor = cnx.cursor()
        # Executa a consulta
        cursor.execute(query, (codigo,))
        # Extrai apenas o primeiro e único resultado da consulta. Isso é importante, pois retorna uma tupla única, e não uma lista de tuplas.
        result = cursor.fetchone()
        # Como é uma consulta de leitura (read-only), não precisa salvar a operação.
        print(result)
    except mysql.connector.Error as e:
        # Como é uma consulta de leitura (read-only), não precisa desfazer a transação em caso de erro.
        print(f"Erro: {e}")
        result = None
    finally:
        # Encerra o cursor
        cursor.close()
        # Devolve a conexão para o pool
        cnx.close()
        # Retorna os resultados da consulta
        return result

# Função DELETE para remover um cliente no banco de dados
def deletar_cliente(codigo):
    global cnx, cursor
    query = """DELETE FROM clientes WHERE codigo = %s"""
    try:
        # Solicita uma conexão ao pool
        cnx = pool.get_connection()
        # Cria um cursor
        cursor = cnx.cursor()
        # Executa o código SQL. Importante que para dados do usuário, esse tipo de método é importante pois evita ataques de SQL Injection.
        cursor.execute(query, (codigo,))
        # Salva (commit) as alterações no banco de dados
        cnx.commit()
        print(f"cliente {codigo} excluído com sucesso.")
    except mysql.connector.Error as e:
        # Se houver erro, desfaz a transação
        cnx.rollback()
        print(f"Erro: {e}")
    finally:
        # Encerra o cursor
        cursor.close()
        # Devolve a conexão para o pool
        cnx.close()
#endregion
def enviar_pedido(cliente, produtos, pagamento, data, hora):
    global cnx, cursor
    codigo_pedido = random.randint(0, 99999)

    query_pedido = """
    INSERT INTO pedidos (numero, codigo_cliente, pagamento, data, hora) VALUES
    (%s, %s, %s, %s, %s)
    """

    try:
        cnx = pool.get_connection()
        cursor = cnx.cursor()

        cursor.execute('SELECT codigo FROM clientes WHERE cpf = %s', (cliente,))
        result = cursor.fetchone()

        if result is None:
            print(f"Cliente com CPF {cliente} não encontrado.")
            return

        cpf_cliente = result[0]

        match pagamento:
            case "Pix":
                pagamento = "pix"
            case "Cartão de crédito":
                pagamento = "cartao_credito"
            case "Cartão de débito":
                pagamento = "cartao_debito"
            case "Dinheiro":
                pagamento = "dinheiro"

        cursor.execute(query_pedido, (codigo_pedido, cpf_cliente, pagamento, data, hora))
        cnx.commit()

        for produto, desconto, observacao, quantidade in produtos:
            query_item = """
            INSERT INTO item_pedido (codigo_pedido, codigo_produto, quantidade, observacao, desconto) 
            VALUES (%s, %s, %s, %s, %s)
            """
            print(quantidade)
            cursor.execute(query_item, (codigo_pedido, produto, quantidade, observacao, desconto))

        cnx.commit()
    except mysql.connector.Error as e:
        cnx.rollback()
        print(e)
    finally:
        cursor.close()
        cnx.close()
