from dataclasses import dataclass, field

import flet as ft


@dataclass(frozen=True)
class CoreSettings:
    title: str = "GUI Sandwich"
    width: int = 540
    height: int = 1212

    db_folder: str = "config"
    db_filename: str = "cfg.json"

    fonts: dict[str, str] = field(default_factory=dict[str, str])


async def init_core(page: ft.Page, cfg: CoreSettings) -> None:
    # Init Fonts
    # Init database
    _init_page(page, cfg)


def _init_page(page: ft.Page, cfg: CoreSettings) -> None:
    page.title = cfg.title
    page.window.width = cfg.width
    page.window.height = cfg.height
