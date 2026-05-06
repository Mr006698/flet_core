import flet as ft

from core import CoreSettings, init_core


async def main(page: ft.Page):
    fonts = {
        "Nunito-Bold": "fonts/Nunito-Bold.ttf",
        "Nunito-Regular": "fonts/Nunito-Regular.ttf",
    }

    settings = CoreSettings(
        title="AGA Clockcard",
        fonts=fonts,
    )

    await init_core(page, settings)


ft.run(main)
