class Produto:
    def __init__(
            self,
            codigo,
            descricao,
            preco,
            quantidadeEstoque
    ):
        self.codigo = codigo
        self.descricao = descricao
        self.preco = preco
        self.quantidadeEstoque = quantidadeEstoque

    def imprime(self):
        print(f'Código: {self.codigo}'
              f'Descrição: {self.descricao}'
              f'Preço: {self.preco}'
              f'Quantidade: {self.quantidadeEstoque}'
              )
class Cliente:
    def __init__(
            self,
            nome,
            cpf,
            telefone,
            endereco
    ):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco

    def alterarCadastro(
            self,
            nome,
            cpf,
            telefone,
            endereco
    ):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco

    def Imprime(self):
        print(
                f'Nome: {self.nome}'
                f'CPF: {self.cpf}'
                f'Telefone: {self.telefone}'
                f'Endereço: {self.endereco}'
            )


class ItemPedido:
    def __init__(
            self,
            quantidade,
            observacao,
            desconto
    ):
        self.quantidade = quantidade
        self.observacao = observacao
        self.desconto = desconto

    def imprime(self):
        print(
            f'Quantidade: {self.quantidade}'
            f'Observação: {self.observacao}'
            f'Desconto: {self.desconto}'
        )