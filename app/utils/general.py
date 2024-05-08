from __future__ import annotations

from typing import Any, Dict


class SingletonMeta(type):
    """
    Metaclass implementing the Singleton design pattern.
    """
    _instances: Dict[SingletonMeta, Any] = {}

    def __call__(cls, *args, **kwargs):
        """
        Override the default behavior of creating instances.
        Ensures that only one instance of the class exists.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

