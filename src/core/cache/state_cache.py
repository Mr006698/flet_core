from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Self


class StateCacheError(Exception): ...


# --- State Cache Base Class --- #
# ------------------------------ #


@dataclass
class _StateCache(ABC):
    _cache: ClassVar[dict[str, Self]] = {}
    _bInit: ClassVar[bool] = False

    @classmethod
    def get(cls) -> Self:
        if not cls._bInit:
            raise StateCacheError("Ensure that SystemState.init has been called!")

        # --- Find the settings class or create it --- #
        if cls.__name__ not in cls._cache:
            cls._cache[cls.__name__] = cls._load()

        return cls._cache[cls.__name__]

    @classmethod
    @abstractmethod
    def _load(cls) -> Self: ...
