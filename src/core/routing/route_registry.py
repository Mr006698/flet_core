import importlib
import pkgutil
from collections.abc import Callable
from functools import wraps

import flet as ft

# --- Load the modules containing the views (Routes) --- #
# ------------------------------------------------------ #


def init_routes() -> None:
    """
    Called to import modules from src.gui folder which in turn
    will call the associated register_route decorator.
    """
    import gui

    for _, module_name, _ in pkgutil.iter_modules(gui.__path__):
        importlib.import_module(f"gui.{module_name}")


# --- Route Registry --- #
# ---------------------- #

type RegisterRouteFunction = Callable[[], ft.View]
_route_register: dict[str, RegisterRouteFunction] = {}


# --- Register Route Decorator --- #
# -------------------------------- #


def register_route(
    route_name: str,
) -> Callable[[RegisterRouteFunction], RegisterRouteFunction]:
    def decorator(fn: RegisterRouteFunction) -> RegisterRouteFunction:
        @wraps(fn)
        def wrapper() -> ft.View:
            return fn()

        _route_register[route_name] = wrapper
        return wrapper

    return decorator


# --- Return The Specified Route (Error Control If None) --- #
# ---------------------------------------------------------- #


def get_route(route_name: str) -> ft.View:
    # --- Get the function object --- #
    route_function = _route_register.get(route_name)
    if route_function is None:
        return ft.View(
            route=route_name,
            controls=[
                ft.Text(
                    f"No route found in _route_registery matching: {route_name}",
                    color=ft.Colors.ERROR,
                )
            ],
        )

    # --- Create the object, note the reference to pop callback --- #
    return route_function()
