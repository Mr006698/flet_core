import flet as ft

from core import CoreSettings, Router, init_core


async def main(page: ft.Page):
    settings = CoreSettings(title="Flet Core")
    await init_core(page, settings)
    page.render_views(Router)


ft.run(main)
