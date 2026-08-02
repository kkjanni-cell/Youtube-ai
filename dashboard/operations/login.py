from auth.auth import authenticate
from auth.session import login_user

from operations.session import login as operations_login


def login_to_operations(username: str, password: str):
    """
    Authenticate the user and initialize both the
    authentication session and the Operations Session.

    Returns:
        dict | None
    """

    user = authenticate(username, password)

    if not user:
        return None

    # Legacy authentication session
    login_user(user)

    # New Operations Session
    operations_login(user)

    return user