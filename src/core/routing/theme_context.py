from dataclasses import dataclass

import flet as ft

from core import State


@ft.observable
@dataclass
class ThemeState(State):
    dark_theme: bool = True
