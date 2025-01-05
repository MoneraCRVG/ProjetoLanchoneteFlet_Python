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
            for codigo, nome, preco, quantidadeEstoque in produtos:
                rows.append(
                    ft.DataRow(
                        [
                            ft.DataCell(ft.Text(f"{codigo}")),
                            ft.DataCell(ft.Text(nome)),
                            ft.DataCell(ft.Text(f"R$ {preco:.2f}")),
                            ft.DataCell(ft.Text(quantidadeEstoque)),
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
            quantidadeEstoque = ft.TextField(label="Quantidade em estoque")

            def enviar(e):
                nome.error_text = ""
                preco.error_text = ""
                quantidadeEstoque.error_text = ""

                _descricao = nome.value
                _preco = preco.value
                _quantidadeEstoque = quantidadeEstoque.value

                if _preco == "":
                    preco.error_text = "Campo obrigatório"
                if _descricao == "":
                    nome.error_text = "Campo obrigatório"
                if _quantidadeEstoque == "":
                    quantidadeEstoque.error_text = "Campo obrigatório"

                if not _preco or not is_decimal(_preco):
                    preco.error_text = "Insira um preço válido"

                if not _quantidadeEstoque or not is_decimal(_quantidadeEstoque):
                    quantidadeEstoque.error_text = "Insira uma quantidade válida"

                if not nome.error_text and not preco.error_text and not quantidadeEstoque.error_text:
                    enviar_produtos(nome.value, preco.value, quantidadeEstoque.value)

            page.views.append(
                ft.View(
                    "/cadastrar-produto",
                    [
                        appbar,
                        nome,
                        preco,
                        quantidadeEstoque,
                        ft.ElevatedButton(text="Enviar", on_click=enviar)
                    ],
                    appbar=appbar,
                    drawer=drawer
                )
            )
        elif page.route == "/editar-produto":
            nome = ft.TextField(label="Descrição", disabled=True)
            preco = ft.TextField(label="Preço", disabled=True)
            quantidadeEstoque = ft.TextField(label="Quantidade em estoque", disabled=True)

            def buscar(e):
                codigo.error_text = ""
                resultado = buscar_produto(codigo.value)
                if resultado:
                    _, nome.value, preco.value, quantidadeEstoque.value = resultado
                    nome.disabled = False
                    quantidadeEstoque.disabled = False
                    preco.disabled = False
                    enviar_botao.disabled = False
                    nome.value = ""
                    quantidadeEstoque.value = ""
                    preco.value = ""
                    enviar_botao.value = ""
                    page.update()
                else:
                    codigo.error_text = "Produto não encontrado!"
                    page.update()

            codigo = ft.TextField(label="Código")

            buscar_botao = ft.ElevatedButton(text="Buscar produto", on_click=buscar)

            def enviar(e):
                editar_produto(codigo.value, nome.value, preco.value, quantidadeEstoque.value)
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
                        quantidadeEstoque,
                        enviar_botao
                    ],
                )
            )
        elif page.route == "/excluir-produto":
            nome = ft.TextField(label="Descrição", disabled=True)
            preco = ft.TextField(label="Preço", disabled=True)
            quantidadeEstoque = ft.TextField(label="Quantidade em estoque", disabled=True)

            def buscar(e):
                codigo.error_text = ""
                resultado = buscar_produto(codigo.value)
                if resultado:
                    _, nome.value, preco.value, quantidadeEstoque.value = resultado
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
                        quantidadeEstoque,
                        deletar_botao

                    ],
                )
            )
        #endregion
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
                            on_click=lambda e: page.go("/cadastrar-cliente")
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.SEARCH,
                            text="Listar clientes",
                            on_click=lambda e: page.go("/lista-clientes")
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.EDIT,
                            text="Alterar clientes",
                            on_click=lambda e: page.go("/editar-cliente")
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.DELETE,
                            text="Excluir clientes",
                            on_click=lambda e: page.go("/excluir-cliente")
                        )
                    ],
                    drawer=drawer,
                    appbar=appbar,
                )
            )
        elif page.route == "/lista-clientes":
            clientes = listar_clientes()

            rows = []
            for codigo, nome, preco, quantidadeEstoque in clientes:
                rows.append(
                    ft.DataRow(
                        [
                            ft.DataCell(ft.Text(f"{codigo}")),
                            ft.DataCell(ft.Text(nome)),
                            ft.DataCell(ft.Text(f"R$ {preco:.2f}")),
                            ft.DataCell(ft.Text(quantidadeEstoque)),
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
                    "/lista-clientes",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK,
                                                  on_click=lambda _: page.go("/clientes"))),
                        table,
                    ],
                    drawer=drawer,
                )
            )
        elif page.route == "/cadastrar-cliente":
            nome = ft.TextField(label="Nome")
            cpf = ft.TextField(label="CPF")
            telefone = ft.TextField(label="Telefone")
            endereco = ft.TextField(label="Endereço")

            def enviar(e):
                nome.error_text = ""
                cpf.error_text = ""
                telefone.error_text = ""
                endereco.error_text = ""

                _nome = nome.value
                _cpf = preco.value
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
                    enviar_clientes(nome.value, preco.value, quantidadeEstoque.value)

            page.views.append(
                ft.View(
                    "/cadastrar-cliente",
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
        elif page.route == "/editar-cliente":
            nome = ft.TextField(label="Nome", disabled=True)
            telefone = ft.TextField(label="Telefone", disabled=True)
            endereco = ft.TextField(label="Endereço", disabled=True)

            def buscar(e):
                resultado = buscar_cliente(cpf.value)
                if resultado:
                    _, nome.value, telefone.value, endereco.value = resultado
                    nome.error_text = ""
                    cpf.error_text = ""
                    telefone.error_text = ""
                    endereco.error_text = ""
                    nome.value = ""
                    cpf.value = ""
                    telefone.value = ""
                    endereco.value = ""
                    page.update()
                else:
                    cpf.error_text = "cliente não encontrado!"
                    page.update()

            cpf = ft.TextField(label="CPF")

            buscar_botao = ft.ElevatedButton(text="Buscar cliente (CPF)", on_click=buscar)

            def enviar(e):
                editar_cliente(codigo.value, nome.value, preco.value, quantidadeEstoque.value)

            enviar_botao = ft.ElevatedButton(text="Salvar alterações", on_click=enviar, disabled=True)

            page.views.append(
                ft.View(
                    "/editar-cliente",
                    [
                        ft.AppBar(leading=ft.IconButton(icon=ft.Icons.ARROW_BACK,
                                                        on_click=lambda _: page.go("/clientes"))),
                        ft.Row([
                            cpf,
                            buscar_botao,
                        ]),
                        nome,
                        telefone,
                        endereco,
                        enviar_botao
                    ],
                )
            )
        elif page.route == "/excluir-cliente":
            nome = ft.TextField(label="Descrição", disabled=True)
            preco = ft.TextField(label="Preço", disabled=True)
            quantidadeEstoque = ft.TextField(label="Quantidade em estoque", disabled=True)

            def buscar(e):
                codigo.error_text = ""
                resultado = buscar_cliente(codigo.value)
                if resultado:
                    _, nome.value, preco.value, quantidadeEstoque.value = resultado
                    page.update()
                else:
                    codigo.error_text = "cliente não encontrado!"
                    page.update()

            codigo = ft.TextField(label="Código")

            buscar_botao = ft.ElevatedButton(text="Buscar cliente", on_click=buscar)

            def enviar_solicitacao_deletar_cliente(e):
                deletar_cliente(codigo.value)

            deletar_botao = ft.ElevatedButton(text="Excluir cliente", on_click=enviar_solicitacao_deletar_cliente)
            page.views.append(
                ft.View(
                    "/excluir-cliente",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK,
                                                  on_click=lambda _: page.go("/clientes"))),
                        ft.Row([
                            codigo,
                            buscar_botao,
                        ]),
                        nome,
                        preco,
                        quantidadeEstoque,
                        deletar_botao

                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


ft.app(main)
