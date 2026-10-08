"""Domain errors."""


class DomainError(Exception):
    """Base class for errors raised by the domain and application layers."""


class NotFoundError(DomainError):
    """A requested resource does not exist."""
