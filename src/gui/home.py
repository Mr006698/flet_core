from datetime import datetime
from functools import partial

import flet as ft

from core import push, register_route
from states.home_state import HomeState


def time_of_day(hour: int) -> str:
    return (
        "Morning" if 0 <= hour <= 11 else "Afternoon" if 12 <= hour <= 17 else "Evening"
    )


@ft.component
def HomeAppBar() -> ft.AppBar:
    home_state, _ = ft.use_state(HomeState.get())
    return ft.AppBar(
        title=ft.Column(
            controls=[
                ft.Text(
                    f"Good {time_of_day(datetime.now().hour)}!",
                    theme_style=ft.TextThemeStyle.TITLE_SMALL,
                    color=ft.Colors.OUTLINE,
                ),
                ft.Text(
                    home_state.username,
                    theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    color=ft.Colors.ON_SURFACE,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            tight=True,
            spacing=0,
        ),
        actions=[
            ft.IconButton(
                icon=ft.Icons.ACCOUNT_CIRCLE,
                icon_color=ft.Colors.PRIMARY,
                tooltip=None,
                icon_size=38,
                on_click=partial(push, "/settings"),
            )
        ],
    )


@register_route("/")
@ft.component
def Home() -> ft.View:
    return ft.View(
        route="/",
        appbar=HomeAppBar(),
        controls=[
            ft.Text("1", size=142, align=ft.Alignment.CENTER),
        ],
    )
