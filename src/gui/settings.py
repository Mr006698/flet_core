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


@register_route("/settings")
@ft.component
def Settings() -> ft.View:
    return ft.View(
        route="/settings",
        appbar=ft.AppBar(title="Settings"),
        bottom_appbar=NavBar(),
        controls=[
            ft.Text("3", size=142, align=ft.Alignment.CENTER),
            ft.TextButton("Back", on_click=pop),
        ],
    )
