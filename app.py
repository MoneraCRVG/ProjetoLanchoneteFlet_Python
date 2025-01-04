import flet as ft
from view import home
def main(page: ft.Page):
    page.title = "Sistema de Lanchonete"
    page.go("/home")


    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        def drawer_handler(e):
            if drawer.selected_index == 0:
                page.go("/home")
            elif drawer.selected_index == 1:
                page.go("/store")

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
        if page.route == "/produtos":
            page.views.append(
                ft.View(
                    "/produtos",
                    [
                        appbar,
                        ft.Text("Bem-vindo ao sistema de produtos"),
                        ft.ElevatedButton(
                            icon=ft.Icons.SEARCH,
                            text="Listar produtos",
                            on_click=lambda e: page.go("/lista-produtos")
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.SEARCH,
                            text="Alterar produtos"
                        ),
                        ft.ElevatedButton(
                            icon=ft.Icons.SEARCH,
                            text="Excluir produtos"
                        )
                    ],
                    drawer=drawer,
                    appbar=appbar,
                )
            )
        elif page.route == "/cadastro-produtos":
            # TODO produtos =
            page.views.append(
                ft.View(
                    "/cadastro-produtos",
                    [
                        appbar,
                    ],
                    drawer=drawer,
                    appbar=appbar,
                )
            )
        page.update()


    page.on_route_change = route_change
    page.go(page.route)


ft.app(main)