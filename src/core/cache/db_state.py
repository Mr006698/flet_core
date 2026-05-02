from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any, ClassVar, Self, cast

from tinydb import TinyDB, where
from tinydb.table import Document

from core.cache.state_cache import _StateCache
from core.cache.system_state import SystemState


class DBStateError(Exception): ...


@dataclass
class DBState(_StateCache):
    """
    The DBState class facilitates persistent storage by loading and saving
    application states directly to a database. By utilizing the DBState.save
    method, the application ensures that user settings and configurations
    remain intact across sessions and reloads.

    Persistence:
    Prevents data loss between application restarts.

    Centralized Storage:
    Uses a database backend for reliable state management.

    Simple Interface:
    Operations are handled primarily through a streamlined save call.

    Logic Flow

    1. Load:
    On initialization, the class retrieves the last known state
    from the database or saves and uses the class defaults.

    2. Modify:
    The application updates settings within the class instance.

    3. Save:
    Invoking DBState.save commits the current configuration to the database,
    ensuring it is available for the next reload.
    """

    _db: ClassVar[TinyDB | None] = None

    def save(self) -> None:
        if self._db is None:
            raise DBStateError("Trying to save when DBState._db is None!")

        # --- Save updated attributes --- #
        cls_name = self.__class__.__name__
        db_table = self._db.table(cls_name)
        for field, value in asdict(self).items():
            db_entry = db_table.get(where(field).exists())
            db_value = cast(Document, db_entry).get(field)
            if db_value != value:
                db_table.update({field: value})

    async def async_save(self) -> None:
        self.save()

    @classmethod
    def _load(cls) -> Self:
        # --- Only create the database once --- #
        if cls._db is None:
            system_state = SystemState.get()
            # --- Check that the path exists --- #
            path = Path(system_state.db_path)
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)

            # --- Create the database --- #
            cls._db = TinyDB(path / system_state.db_filename)

        # --- Check the saved settings against the defaults --- #
        cls_dict = cls._load_db_settings(cls._db)

        return cls(**cls_dict)

    @classmethod
    def _load_db_settings(cls, db: TinyDB) -> dict[str, Any]:
        field_names = [field.name for field in fields(cls)]
        cls_dict = {field: getattr(cls, field) for field in field_names}

        db_table = db.table(cls.__name__)
        for field, value in cls_dict.items():
            db_entry = db_table.get(where(field).exists())
            if db_entry is None:
                db_table.insert({field: value})
                continue

            db_value = cast(Document, db_entry).get(field)
            if db_value != value:
                cls_dict[field] = db_value

        return cls_dict

    # def __init_subclass__(cls) -> None:
    #     print(f"Called: {cls.__name__}")
    #     return super().__init_subclass__()
