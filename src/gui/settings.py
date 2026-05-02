import flet as ft

from core import pop, register_route
from core.routing.theme_context import ThemeState
from states.home_state import HomeState

# --- Standardized ListTile Control --- #
# ------------------------------------- #


@ft.control
class SettingTile(ft.ListTile):
    def init(self):
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_LOW
        self.shape = ft.RoundedRectangleBorder(radius=10)
        self.title_text_style = ft.TextStyle(
            size=16,
            font_family="Nunito-Bold",
            color=ft.Colors.ON_SURFACE,
        )
        self.subtitle_text_style = ft.TextStyle(
            size=16,
            font_family="Nunito-Regular",
            color=ft.Colors.OUTLINE,
        )


# --- Standardized Setting Heading Control --- #
# -------------------------------------------- #


def SettingHeading(title: str) -> ft.Text:
    return ft.Text(
        title,
        font_family="Nunito-Bold",
        theme_style=ft.TextThemeStyle.BODY_MEDIUM,
    )


# --- Username Setting --- #
# ------------------------ #


@ft.component
def UserNameSetting() -> ft.Control:
    home_state, _ = ft.use_state(HomeState.get())

    edit_name = ft.TextField(home_state.username)

    def save_username() -> None:
        home_state.username = edit_name.value
        home_state.save()
        ft.context.page.pop_dialog()

    def set_username() -> None:
        ok_btn = ft.Button("OK", on_click=save_username)
        cancel_btn = ft.Button("Cancel", on_click=ft.context.page.pop_dialog)

        dlg = ft.AlertDialog(
            title=ft.Text(
                "Edit Name",
                font_family="Nunito-Bold",
                theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
            ),
            content=edit_name,
            actions=[ok_btn, cancel_btn],
            modal=True,
        )
        ft.context.page.show_dialog(dlg)

    return SettingTile(
        title="Edit name",
        subtitle=home_state.username,
        on_click=set_username,
    )


# --- Theme Mode Setting --- #
# -------------------------- #


@ft.component
def ThemeModeToggle() -> ft.Control:
    theme, _ = ft.use_state(ThemeState.get())

    def toggle() -> None:
        theme.dark_theme = not theme.dark_theme
        theme.save()

    return ft.Switch(value=theme.dark_theme, on_change=toggle)


def ThemeModeSetting() -> ft.Control:
    return SettingTile(
        title="Dark theme",
        subtitle="Switch between light and dark theme mode",
        trailing=ThemeModeToggle(),
    )


# --- Main Settings View Control --- #
# ---------------------------------- #


@register_route("/settings")
@ft.component
def Settings() -> ft.View:
    return ft.View(
        route="/settings",
        appbar=ft.AppBar(
            title=ft.Text(
                "Settings",
                font_family="Nunito-Bold",
                theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
            )
        ),
        controls=[
            SettingHeading("Username"),
            UserNameSetting(),
            SettingHeading("Appearance"),
            ThemeModeSetting(),
            ft.TextButton("Back", on_click=pop),
        ],
    )
