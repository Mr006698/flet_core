from dataclasses import dataclass

import flet as ft

from core import DBState


@ft.observable
@dataclass
class ThemeState(DBState):
    dark_theme: bool = True
