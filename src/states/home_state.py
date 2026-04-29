from dataclasses import dataclass

import flet as ft

from core import DBState


@ft.observable
@dataclass
class HomeState(DBState):
    username: str = "Username"
