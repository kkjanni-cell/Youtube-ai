"""
Role definitions for the Operations Console.

This module defines which permissions are granted to each role.
It should contain only role and permission mappings.
"""

ROLES = {
    "Viewer": {
        "dashboard.view",
    },

    "Operator": {
        "dashboard.view",
        "tracking.view",
        "tracking.create",
        "tracking.edit",
    },

    "Admin": {
        "dashboard.view",
        "tracking.view",
        "tracking.create",
        "tracking.edit",
        "users.manage",
        "settings.manage",
    },
}