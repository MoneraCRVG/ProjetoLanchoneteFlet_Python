CREATE DATABASE IF NOT EXISTS 'lanchonete_sabrina';


CREATE TABLE 'lanchonete_sabrina'.'cliente' (
    id INT PRIMARY NOT NULL,
    telefone VARCHAR(16) NOT NULL,
    cpf CHAR(11) NOT NULL,
    nome VARCHAR(32),
    endereco VARCHAR(64),
)
CREATE TABLE 'lanchonete_sabrina'.'produto' (
    id INT PRIMARY NOT NULL,
    quantidade INT NOT NULL,
    observacao TEXT,
    desconto FLOAT(2,2) NOT NULL,
)
CREATE TABLE 'lanchonete_sabrina'.'pedido' (

)