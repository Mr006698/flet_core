from functools import partial

import flet as ft

from core import home, pop, push, register_route


@ft.component
def NavBar() -> ft.BottomAppBar:
    return ft.BottomAppBar(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.TextButton("Home", on_click=home),
                ft.TextButton("Page 1", on_click=partial(push, "/")),
                ft.TextButton("Page 2", on_click=partial(push, "/details")),
                ft.TextButton("Page 3", on_click=partial(push, "/settings")),
                ft.TextButton("Back", on_click=pop),
            ],
        )
    )


@register_route("/")
@ft.component
def Home() -> ft.View:
    return ft.View(
        route="/",
        appbar=ft.AppBar(title="Home"),
        bottom_appbar=NavBar(),
        controls=[
            ft.Text("1", size=142, align=ft.Alignment.CENTER),
        ],
    )
