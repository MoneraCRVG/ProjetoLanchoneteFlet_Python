import datetime

import flet as ft
from database.lanchonete_sabrina_db import *

def is_decimal(s):
    s = s.strip()
    if s.count('.') == 1 and s.replace('.', '', 1).isdigit() and s != '.':
        return True
    try:
        float(s)
        return True
    except ValueError:
        return False


def main(page: ft.Page):
    page.title = "Sistema de Lanchonete"
    page.go("/home")

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        def drawer_handler(e):
            if drawer.selected_index == 0:
                page.go("/home")
            elif drawer.selected_index == 1:
                page.go("/clientes")
            elif drawer.selected_index == 2:
                page.go("/produtos")

        drawer = ft.NavigationDrawer(
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Página inicial",
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME_FILLED,
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="Clientes",
                    icon=ft.Icon(ft.Icons.PERSON_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.PERSON)
                ),
                ft.NavigationDrawerDestination(
                    label="Produtos",
                    icon=ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.SHOPPING_CART),
                )
            ],
            on_change=drawer_handler
        )
        button = ft.IconButton(icon=ft.Icons.MENU, on_click=lambda e: page.open(drawer))
        appbar = ft.AppBar(
            leading=button,
            title=ft.Text("Sistema de Lanchonete"),
        )
        page.views.append(
            ft.View(
                "/home",
                [
                    appbar,
                    ft.Column(
                        controls=[
                            ft.Text("Bem-vindo ao Sistema de Lanchonete!", size=30, weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK),

                            # Botão Produtos
                            ft.ElevatedButton(
                                text="Produtos",
                                icon=ft.Icons.SHOPPING_CART,
                                on_click=lambda e: page.go("/produtos"),
                            ),

                            # Botão Clientes
                            ft.ElevatedButton(
                                text="Clientes",
                                icon=ft.Icons.PERSON,
                                on_click=lambda e: page.go("/clientes"),
                            ),

                            # Botão Novo Pedido
                            ft.ElevatedButton(
                                text="Novo Pedido",
                                icon=ft.Icons.ADD_SHOPPING_CART,
                                on_click=lambda e: page.go("/novo-pedido"),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20

                    )
                ],
                drawer=drawer,
                appbar=appbar,
            )
        )
        # region Produtos
        if page.route == "/produtos":
            page.views.append(
                ft.View(
                    "/produtos",
                    [
                        appbar,
                        ft.Text("Bem-vindo ao sistema de produtos"),
                        ft.ElevatedButton(
                            icon=ft.Icons.ADD,
                            text="Cadastrar produtos",
                            on_click=lambda e: page.go("/cadastrar-produto")
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.SEARCH,
                            text="Listar produtos",
                            on_click=lambda e: page.go("/lista-produtos")
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.EDIT,
                            text="Alterar produtos",
                            on_click=lambda e: page.go("/editar-produto")
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.DELETE,
                            text="Excluir produtos",
                            on_click=lambda e: page.go("/excluir-produto")
                        )
                    ],
                    drawer=drawer,
                    appbar=appbar,
                )
            )
        elif page.route == "/lista-produtos":
            produtos = listar_produtos()

            rows = []
            for codigo, nome, preco, quantidade in produtos:
                rows.append(
                    ft.DataRow(
                        [
                            ft.DataCell(ft.Text(f"{codigo}")),
                            ft.DataCell(ft.Text(nome)),
                            ft.DataCell(ft.Text(f"R$ {preco:.2f}")),
                            ft.DataCell(ft.Text(quantidade)),
                        ]
                    )
                )

            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Código")),
                    ft.DataColumn(ft.Text("Descrição")),
                    ft.DataColumn(ft.Text("Preço")),
                    ft.DataColumn(ft.Text("Quantidade em Estoque")),
                ],
                rows=rows
            )
            page.views.append(
                ft.View(
                    "/lista-produtos",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/produtos"))),
                        table,
                    ],
                    drawer=drawer,
                )
            )
        elif page.route == "/cadastrar-produto":
            nome = ft.TextField(label="Descrição")
            preco = ft.TextField(label="Preço")
            quantidade = ft.TextField(label="Quantidade em estoque")

            def enviar(e):
                nome.error_text = ""
                preco.error_text = ""
                quantidade.error_text = ""

                _descricao = nome.value
                _preco = preco.value
                _quantidadeEstoque = quantidade.value

                if _preco == "":
                    preco.error_text = "Campo obrigatório"
                if _descricao == "":
                    nome.error_text = "Campo obrigatório"
                if _quantidadeEstoque == "":
                    quantidade.error_text = "Campo obrigatório"

                if not _preco or not is_decimal(_preco):
                    preco.error_text = "Insira um preço válido"

                if not _quantidadeEstoque or not is_decimal(_quantidadeEstoque):
                    quantidade.error_text = "Insira uma quantidade válida"

                if not nome.error_text and not preco.error_text and not quantidade.error_text:
                    enviar_produtos(nome.value, preco.value, quantidade.value)

            page.views.append(
                ft.View(
                    "/cadastrar-produto",
                    [
                        appbar,
                        nome,
                        preco,
                        quantidade,
                        ft.ElevatedButton(text="Enviar", on_click=enviar)
                    ],
                    appbar=appbar,
                    drawer=drawer
                )
            )
        elif page.route == "/editar-produto":
            nome = ft.TextField(label="Descrição", disabled=True)
            preco = ft.TextField(label="Preço", disabled=True)
            quantidade = ft.TextField(label="Quantidade em estoque", disabled=True)

            def buscar(e):
                codigo.error_text = ""
                resultado = buscar_produto(codigo.value)
                if resultado:
                    _, nome.value, preco.value, quantidade.value = resultado
                    nome.disabled = False
                    quantidade.disabled = False
                    preco.disabled = False
                    enviar_botao.disabled = False
                    nome.value = ""
                    quantidade.value = ""
                    preco.value = ""
                    enviar_botao.value = ""
                    page.update()
                else:
                    codigo.error_text = "Produto não encontrado!"
                    page.update()

            codigo = ft.TextField(label="Código")

            buscar_botao = ft.ElevatedButton(text="Buscar produto", on_click=buscar)

            def enviar(e):
                editar_produto(codigo.value, nome.value, preco.value, quantidade.value)
            enviar_botao = ft.ElevatedButton(text="Salvar alterações", on_click=enviar, disabled=True)

            page.views.append(
                ft.View(
                    "/editar-produto",
                    [
                        ft.AppBar(leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/produtos"))),
                        ft.Row([
                            codigo,
                            buscar_botao,
                        ]),
                        nome,
                        preco,
                        quantidade,
                        enviar_botao
                    ],
                )
            )
        elif page.route == "/excluir-produto":
            nome = ft.TextField(label="Descrição", disabled=True)
            preco = ft.TextField(label="Preço", disabled=True)
            quantidade = ft.TextField(label="Quantidade em estoque", disabled=True)

            def buscar(e):
                codigo.error_text = ""
                resultado = buscar_produto(codigo.value)
                if resultado:
                    _, nome.value, preco.value, quantidade.value = resultado
                    page.update()
                else:
                    codigo.error_text = "Produto não encontrado!"
                    page.update()
            codigo = ft.TextField(label="Código")

            buscar_botao = ft.ElevatedButton(text="Buscar produto", on_click=buscar)

            def enviar_solicitacao_deletar_produto(e):
                deletar_produto(codigo.value)

            deletar_botao = ft.ElevatedButton(text="Excluir produto", on_click=enviar_solicitacao_deletar_produto)
            page.views.append(
                ft.View(
                    "/excluir-produto",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/produtos"))),
                        ft.Row([
                            codigo,
                            buscar_botao,
                        ]),
                        nome,
                        preco,
                        quantidade,
                        deletar_botao

                    ],
                )
            )
        #endregion
        # region Clientes
        elif page.route == "/clientes":
            page.views.append(
                ft.View(
                    "/clientes",
                    [
                        appbar,
                        ft.Text("Bem-vindo ao sistema de clientes"),
                        ft.ElevatedButton(
                            icon=ft.Icons.ADD,
                            text="Cadastrar clientes",
                            on_click=lambda e: page.go("/cadastrar-cpf_cliente")
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.SEARCH,
                            text="Listar clientes",
                            on_click=lambda e: page.go("/lista-clientes")
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.EDIT,
                            text="Alterar clientes",
                            on_click=lambda e: page.go("/editar-cpf_cliente")
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.DELETE,
                            text="Excluir clientes",
                            on_click=lambda e: page.go("/excluir-cpf_cliente")
                        )
                    ],
                    drawer=drawer,
                    appbar=appbar,
                )
            )
        elif page.route == "/lista-clientes":
            clientes = listar_clientes()

            rows = []
            for codigo, cpf, nome, telefone, endereco in clientes:
                rows.append(
                    ft.DataRow(
                        [
                            ft.DataCell(ft.Text(codigo)),
                            ft.DataCell(ft.Text(cpf)),
                            ft.DataCell(ft.Text(nome)),
                            ft.DataCell(ft.Text(telefone)),
                            ft.DataCell(ft.Text(endereco)),
                        ]
                    )
                )

            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Código")),
                    ft.DataColumn(ft.Text("CPF")),
                    ft.DataColumn(ft.Text("Nome")),
                    ft.DataColumn(ft.Text("Telefone")),
                    ft.DataColumn(ft.Text("Endereço")),
                ],
                rows=rows
            )
            page.views.append(
                ft.View(
                    "/lista-clientes",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/clientes"))),
                        table,
                    ],
                    drawer=drawer,
                )
            )
        elif page.route == "/cadastrar-cpf_cliente":
            nome = ft.TextField(label="Nome")
            cpf = ft.TextField(label="CPF")
            endereco = ft.TextField(label="Endereço")
            telefone = ft.TextField(label="Telefone")

            def enviar(e):
                nome.error_text = ""
                cpf.error_text = ""
                telefone.error_text = ""
                endereco.error_text = ""

                _nome = nome.value
                _cpf = cpf.value
                _telefone = telefone.value
                _endereco = endereco.value

                if _nome == "":
                    nome.error_text = "Campo obrigatório"
                if _cpf == "":
                    cpf.error_text = "Campo obrigatório"
                if _telefone == "":
                    telefone.error_text = "Campo obrigatório"
                if _endereco == "":
                    endereco.error_text = "Campo obrigatório"

                if not nome.error_text and not cpf.error_text and not telefone.error_text and not endereco.error_text:
                    enviar_clientes(cpf.value, nome.value, telefone.value, endereco.value)

            page.views.append(
                ft.View(
                    "/cadastrar-cpf_cliente",
                    [
                        appbar,
                        nome,
                        cpf,
                        telefone,
                        endereco,
                        ft.ElevatedButton(text="Enviar", on_click=enviar)
                    ],
                    appbar=appbar,
                    drawer=drawer
                )
            )
        elif page.route == "/editar-cpf_cliente":
            codigo = ft.TextField(label="Código")
            nome = ft.TextField(label="Nome", disabled=True)
            telefone = ft.TextField(label="Telefone", disabled=True)
            endereco = ft.TextField(label="Endereço", disabled=True)
            cpf = ft.TextField(label="CPF", disabled=True)

            def buscar(e):
                resultado = buscar_cliente(codigo.value)
                if resultado:
                    nome.error_text = ""
                    cpf.error_text = ""
                    telefone.error_text = ""
                    endereco.error_text = ""
                    nome.value = ""
                    cpf.value = ""
                    telefone.value = ""
                    endereco.value = ""
                    _,cpf.value, nome.value, telefone.value, endereco.value = resultado

                    nome.disabled = False
                    cpf.disabled = False
                    telefone.disabled = False
                    endereco.disabled = False
                    enviar_botao.disabled = False
                    page.update()
                else:
                    codigo.error_text = "Cliente não encontrado!"
                    page.update()


            buscar_botao = ft.ElevatedButton(text="Buscar cpf_cliente", on_click=buscar)

            def enviar(e):
                editar_cliente(codigo.value, cpf.value, nome.value, telefone.value, endereco.value)

            enviar_botao = ft.ElevatedButton(text="Salvar alterações", on_click=enviar, disabled=True)
            page.views.append(
                ft.View(
                    "/editar-cpf_cliente",
                    [
                        ft.AppBar(leading=ft.IconButton(icon=ft.Icons.ARROW_BACK,
                                                        on_click=lambda _: page.go("/clientes"))),
                        ft.Row([
                            codigo,
                            buscar_botao,
                        ]),
                        cpf,
                        nome,
                        telefone,
                        endereco,
                        enviar_botao
                    ],
                )
            )
        elif page.route == "/excluir-cpf_cliente":
            cpf = ft.TextField(label="CPF", disabled=True)
            nome = ft.TextField(label="Descrição", disabled=True)
            preco = ft.TextField(label="Preço", disabled=True)
            quantidade = ft.TextField(label="Quantidade em estoque", disabled=True)


            def buscar(e):
                codigo.error_text = ""
                resultado = buscar_cliente(codigo.value)
                if resultado:
                    _, cpf.value, nome.value, preco.value, quantidade.value = resultado
                    deletar_botao.disabled = False
                    page.update()
                else:
                    codigo.error_text = "cpf_cliente não encontrado!"
                    page.update()

            codigo = ft.TextField(label="Código")

            buscar_botao = ft.ElevatedButton(text="Buscar cpf_cliente", on_click=buscar)

            def enviar_solicitacao_deletar_cliente(e):
                deletar_cliente(codigo.value)
                deletar_botao.disabled = True


            deletar_botao = ft.ElevatedButton(text="Excluir cpf_cliente", on_click=enviar_solicitacao_deletar_cliente, disabled=True)
            page.views.append(
                ft.View(
                    "/excluir-cpf_cliente",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK,
                                                  on_click=lambda _: page.go("/clientes"))),
                        ft.Row([
                            codigo,
                            buscar_botao,
                        ]),
                        cpf,
                        nome,
                        preco,
                        quantidade,
                        deletar_botao
                    ],
                )
            )
        #endregion
        #region Novo Pedido
        elif page.route == "/novo-pedido":
            data = datetime.date.today()
            hora = datetime.datetime.now().time()

            pagamento = ft.Dropdown(
                options=[
                    ft.dropdown.Option("Pix"),
                    ft.dropdown.Option("Cartão de crédito"),
                    ft.dropdown.Option("Cartão de débito"),
                    ft.dropdown.Option("Dinheiro")
                ],
                label="Método de pagamento",
                width=300
            )

            cpf_cliente = ft.TextField(label="CPF do cliente")
            produto = ft.TextField(label="Código do produto")
            produtos_selecionados = []

            def adicionar_produto(e):
                if produto.value:
                    produtos_selecionados.append((produto.value, desconto.value, observacao.value, quantidade.value))
                    produto.value = ""
                    desconto.value = ""
                    observacao.value = ""
                    quantidade.value = ""
                    page.update()

            def enviar_pedido_button(e):
                lista_produtos = []
                for produto.value in produtos_selecionados:
                    lista_produtos.append(produto.value)

                cliente_selecionado = cpf_cliente.value
                if cliente_selecionado and produtos_selecionados and pagamento.value:
                    enviar_pedido(cliente_selecionado, lista_produtos, pagamento.value, data, hora)
                else:
                    page.add(ft.Text("Preencha todos os campos antes de enviar o pedido.", color="red"))
                    page.update()

            adicionar_produto_button = ft.ElevatedButton("Adicionar Produto", on_click=adicionar_produto)

            enviar_button = ft.ElevatedButton(text="Enviar Pedido", on_click=enviar_pedido_button)
            desconto = ft.TextField(label="Desconto (%)")
            observacao = ft.TextField(label="Observação")
            quantidade = ft.TextField(label="Quantidade")
            page.views.append(
                ft.View(
                    "/novo-produto",
                    controls=[
                        ft.AppBar(
                            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK,
                                                  on_click=lambda _: page.go("/home"))),
                        cpf_cliente,
                        ft.Row([
                            produto,
                            desconto,
                            observacao,
                            quantidade,
                        ]),
                        adicionar_produto_button,
                        ft.Text("Produtos selecionados:"),
                        ft.Column([ft.Text(produto) for produto in produtos_selecionados]),
                        pagamento,
                        enviar_button
                    ],
                    spacing=20
                )
            )
        #endregion
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


ft.app(main)
