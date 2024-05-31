"""Declares every entity type and it's representation."""
from enum import Enum


class EntityType(Enum):
    """Declares every entity type."""
    HEALTHY: str = '*' # type: ignore
    IMMUNE: str = '~' # type: ignore
    INFECTED: str = 'O' # type: ignore
    DEAD: str = '+' # type: ignore
    HEALED: str = '.' # type: ignore
