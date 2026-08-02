from operations.roles import ROLES
from operations.session import get_session


def get_permissions() -> set[str]:
    """
    Return the permissions for the current user's role.
    """

    session = get_session()
    role = session["role"]

    return ROLES.get(role, set())


def can(permission: str) -> bool:
    """
    Return True if the current user has the requested permission.
    """

    return permission in get_permissions()