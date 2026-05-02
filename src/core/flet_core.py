from dataclasses import dataclass, field

import flet as ft

from core.cache.system_state import SystemState
from core.routing.route_registry import _init_routes
from core.routing.router_control import Router


@dataclass(frozen=True)
class CoreSettings:
    title: str = "GUI Sandwich"
    width: int = 540
    height: int = 1212

    db_folder: str = "config"
    db_filename: str = "cfg.json"

    fonts: dict[str, str] = field(default_factory=dict[str, str])


async def init_core(page: ft.Page, cfg: CoreSettings) -> None:
    await SystemState.init(cfg.db_folder, cfg.db_filename)
    _init_fonts(page, cfg.fonts)
    _init_page(page, cfg)
    _init_routes()

    page.render_views(Router)


def _init_fonts(page: ft.Page, fonts: dict[str, str]) -> None:
    if not fonts:
        return

    page.fonts = fonts


def _init_page(page: ft.Page, cfg: CoreSettings) -> None:
    page.title = cfg.title
    page.window.width = cfg.width
    page.window.height = cfg.height
