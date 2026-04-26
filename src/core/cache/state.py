from dataclasses import dataclass
from typing import Self

from core.cache.state_cache import _StateCache


@dataclass
class State(_StateCache):
    @classmethod
    def _load(cls) -> Self:
        return cls()
