from collections.abc import Generator
from dataclasses import dataclass, field
from typing import NamedTuple

import flet as ft

# --- History Data --- #
# -------------------- #


class History(NamedTuple):
    route: str
    query: dict[str, str]


@dataclass(frozen=True)
class HistoryStack:
    """
    This dataclass is frozen to prevent Flet from updating views during
    pop events.
    By using an immutable object within the RouterModel, we ensure that
    the HistoryStack itself cannot be modified, while the data it contains
    can still be updated.
    """

    _stack: list[History] = field(default_factory=list[History])

    def pop(self) -> History:
        if len(self._stack) > 1:
            self._stack.pop()
            return self._stack.pop()

        return self._stack[0]

    def add(self, route: str, query: dict[str, str]) -> History:
        history = History(route, query)
        self._stack.append(history)
        return history

    def home(self) -> History:
        """
        Resets the navigation stack to the home route.

        Note: Flet suppresses route change events if the target view matches the
        current view. To prevent an empty stack when 'home' is called on an already
        active home route, this method clears the stack history but retains the
        first entry. This ensures `RouterState.home` can update the default route
        and trigger a UI redraw instead of a route change event triggering
        HistoryStack.add to push it back onto the list.
        """
        # --- Clear all of the stack --- #
        if len(self._stack) > 1:
            # Flet route event will be called so delete and return
            # popped route and let the event handle it.
            del self._stack[1:]
            return self._stack.pop()

        # As home is called on the home route flet route event will not
        # be called so return the last entry in the stack. But don't pop it.
        return self._stack[0]


# --- Router State Class --- #
# -------------------------- #


@ft.observable
@dataclass
class RouterState:
    """
    Holds the route history used to determine which view names should be
    built via the router_registry. The default_route exists primarily to
    ensure updates are triggered only when routes are added.
    """

    history: HistoryStack
    query: dict[str, str] = field(default_factory=dict[str, str], init=False)
    default_route: str = ""

    def add(self, route: str, query: dict[str, str]) -> None:
        self.default_route, self.query = self.history.add(route, query)

    def pop(self) -> History:
        return self.history.pop()

    def home(self) -> History:
        return self.history.home()

    def routes(self) -> Generator[History, None, None]:
        return (history for history in self.history._stack)
