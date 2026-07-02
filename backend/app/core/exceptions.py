class DomainError(Exception):
    """Base exception for domain rule violations."""


class NotFoundError(DomainError):
    """Raised when a requested entity does not exist."""
