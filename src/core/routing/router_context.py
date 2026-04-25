import flet as ft
from flet.components.hooks.use_context import ContextProvider

from core.routing.router_state import History, HistoryStack, RouterState

# --- RouterContextError --- #
# -------------------------- #


class RouterContextError(Exception): ...


# --- Router Context --- #
# ---------------------- #


class _ContextCache:
    def __init__(self) -> None:
        self.state: RouterState | None = None
        self.ctx: ContextProvider[RouterState] | None = None


_ctx_cache = _ContextCache()


def get_router_state() -> RouterState:
    if _ctx_cache.state is None:
        try:
            _ctx_cache.state = RouterState(
                default_route=ft.context.page.route,
                history=HistoryStack([History(ft.context.page.route, {})]),
            )

        except RuntimeError:
            raise RouterContextError(
                "Trying to set router context outside of flet context."
            )

    return _ctx_cache.state


def get_router_context() -> ContextProvider[RouterState]:
    if _ctx_cache.ctx is None:
        _ctx_cache.ctx = ft.create_context(get_router_state())

    return _ctx_cache.ctx


async def pop() -> None:
    if _ctx_cache.state is None:
        raise RouterContextError("Using pop on uninitialised _ContextCache.")

    history = _ctx_cache.state.pop()
    await ft.context.page.push_route(history.route, **history.query)


# --- Go to home route and reset history stack --- #
async def home() -> None:
    if _ctx_cache.state is None:
        raise RouterContextError("Using home on uninitialised _ContextCache.")

    history = _ctx_cache.state.home()
    await ft.context.page.push_route(history.route)


# --- Get the page querys --- #
def query() -> dict[str, str]:
    if _ctx_cache.state is None:
        raise RouterContextError("Using query on uninitialised _ContextCache.")

    return _ctx_cache.state.query


async def push(
    route: str,
    ev: ft.ControlEvent | None = None,
    **query,
) -> None:
    try:
        await ft.context.page.push_route(route, **query)

    except RuntimeError:
        raise RouterContextError("Trying to push route outside of flet context.")
