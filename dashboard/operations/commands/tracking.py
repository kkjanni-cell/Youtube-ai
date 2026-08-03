from dashboard.operations.models.command import Command
from dashboard.operations.services.registry import registry


def add_tracking():
    print("Track Video")


registry.register(
    Command(
        id="tracking.add",
        title="Add Tracking",
        category="Tracking",
        permission="tracking.write",
        handler=add_tracking,
        icon="➕",
        description="Track a new YouTube video",
    )
)