from dashboard.operations.models.command import Command


class CommandRegistry:
    """
    Stores every available command in the application.
    """

    def __init__(self):
        self._commands: dict[str, Command] = {}

    def register(self, command: Command):
        self._commands[command.id] = command

    def unregister(self, command_id: str):
        self._commands.pop(command_id, None)

    def get(self, command_id: str):
        return self._commands.get(command_id)

    def all(self):
        return list(self._commands.values())


registry = CommandRegistry()