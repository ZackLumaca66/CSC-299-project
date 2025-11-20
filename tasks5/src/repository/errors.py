"""Repository error classes."""

class RepositoryError(Exception):
    """Base error for repository problems."""


class CorruptDataError(RepositoryError):
    """Raised when underlying JSON data is corrupt and has been reset."""


class AtomicWriteError(RepositoryError):
    """Raised when atomic write sequence fails."""