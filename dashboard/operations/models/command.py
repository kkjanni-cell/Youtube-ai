from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(slots=True)
class Command:
    """
    Represents a single operation that can be executed
    from the Operations Console.
    """

    id: str
    title: str
    category: str
    permission: str

    handler: Callable

    description: str = ""
    icon: str = ""
    shortcut: Optional[str] = None