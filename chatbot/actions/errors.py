class InvalidUserError(RuntimeError):
    """User is not allowed to have access to actions"""


class BackendError(RuntimeError):
    """Something went wrong while accessing the backend"""
