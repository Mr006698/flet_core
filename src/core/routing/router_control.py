import flet as ft

from core.routing.route_registry import get_route
from core.routing.router_context import get_router_context
from core.routing.router_state import History, HistoryStack, RouterState
from core.routing.theme_context import THEME_CONTEXT

# --- Router Class --- #
# -------------------- #


@ft.component
def Router() -> list[ft.View]:
    # --- Create the router model --- #
    router, _ = ft.use_state(
        RouterState(
            default_route=ft.context.page.route,
            history=HistoryStack([History(ft.context.page.route, {})]),
        )
    )

    # --- Set the router context with the state (run once) --- #
    router = ft.use_context(get_router_context())

    # --- Theme mode context value --- #
    theme_mode_context = ft.use_context(THEME_CONTEXT)

    # --- Page route events (keep flet controls out of models) --- #
    def route_changed(ev: ft.RouteChangeEvent) -> None:
        # --- Parse query string --- #
        params = ev.route.split("?")[0]
        query = ft.context.page.query.to_dict
        router.add(params, query)

    async def pop() -> None:
        history = router.pop()
        await ft.context.page.push_route(history.route, **history.query)

    # --- Subscribe to page route events --- #
    ft.context.page.on_route_change = route_changed
    ft.context.page.on_view_pop = pop

    # --- Update the theme mode if changed --- #
    def update_theme_mode() -> None:
        mode = (
            ft.ThemeMode.DARK if theme_mode_context.dark_theme else ft.ThemeMode.LIGHT
        )
        ft.context.page.theme_mode = mode

    ft.on_updated(update_theme_mode, dependencies=[theme_mode_context.dark_theme])

    # --- Create the view list from the history stack --- #
    return [
        # TODO: Fix route_registry.py to accept RouterContext for now.
        get_route(history.route)
        for history in router.routes()
    ]
