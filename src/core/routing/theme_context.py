from dataclasses import dataclass

import flet as ft


@ft.observable
@dataclass
class ThemeState:
    dark_theme: bool = True


THEME_CONTEXT = ft.create_context(ThemeState())
