import flet as ft

from core import CoreSettings, init_core


async def main(page: ft.Page):
    fonts = {
        "fonts/Nunito-Bold.ttf": "Nunito-Bold",
        "fonts/Nunito-Regular.ttf": "Nunito-Regular",
    }

    settings = CoreSettings(
        title="AGA Clockcard",
        fonts=fonts,
    )

    await init_core(page, settings)


ft.run(main)
