import flet as ft
texto = ft.Text("Bem-vindo ao Sistema de Lanchonete!")

container = ft.Column(
    controls=[
        texto,
        ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icon(ft.icons.PERSON_OUTLINED),
                    selected_icon=ft.Icon(ft.icons.PERSON_OUTLINED),
                    on_click=lambda e: page.go("/store")
                )
            ]
        )
    ]
)

