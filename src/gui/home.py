from functools import partial

import flet as ft

from core import home, pop, push, register_route
from states.home_state import HomeState


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


@ft.component
def NameChange(state: HomeState) -> ft.Control:

    text_field = ft.TextField(value=state.username, expand=True)

    def set_name() -> None:
        state.username = text_field.value
        # state.save()

    button = ft.Button("Set name", on_click=set_name)
    return ft.Row(controls=[text_field, button])


@register_route("/")
@ft.component
def Home() -> ft.View:
    home_state, _ = ft.use_state(HomeState.get())

    # ft.on_updated(home_state.save, [home_state.username])

    return ft.View(
        route="/",
        appbar=ft.AppBar(title=home_state.username),
        bottom_appbar=NavBar(),
        controls=[
            NameChange(home_state),
            ft.Text("1", size=142, align=ft.Alignment.CENTER),
        ],
    )
