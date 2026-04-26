from dataclasses import dataclass
from pathlib import Path
from typing import Self

import flet as ft

from core.cache.state_cache import _StateCache


@dataclass
class SystemState(_StateCache):
    """
    Base state class containing system dependant settings
    such as system paths etc.

    SystemState.init must be called before any other operations on
    DBState classes as the directories need to be present to allow
    for the saving of the state data.
    """

    cache_dir: str = ""
    db_path: str = ""
    db_filename: str = ""

    @classmethod
    def _load(cls) -> Self:
        return cls(cls.cache_dir, cls.db_path, cls.db_filename)

    @classmethod
    async def init(cls, db_folder: str, db_filename) -> None:
        """
        Must be called at project start to initialise system specific
        settings such as system directories.

        Method will only run once. Subsequent calls will be ignored.

        Args:
            db_folder (str): folder to store json file.
            db_filename (str): name of the json file.
        """

        if _StateCache._bInit:
            return

        # --- Just get the system dependant directories --- #
        cls.cache_dir = await ft.StoragePaths().get_application_cache_directory()

        # --- Create the database path --- #
        db_path = Path(cls.cache_dir) / db_folder
        cls.db_path = db_path.as_posix()
        cls.db_filename = db_filename

        _StateCache._bInit = True
