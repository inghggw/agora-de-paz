from enum import Enum


class ParticipantMode(str, Enum):
    """Doble carril de participación (ver docs/01-problema-y-vision.md, principio 4)."""

    VERIFIED = "verified"
    ANONYMOUS = "anonymous"
