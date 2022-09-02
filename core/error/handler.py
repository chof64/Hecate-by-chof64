"""Main entrypoint for caught errors and exception."""

from .loggers import UncaughtLogger


class ErrorHandler:  # pylint: disable=too-few-public-methods
    """
    Responsible for classifying errors and exceptions.
    """

    def __init__(self, bot):
        self.bot = bot

    async def handle(self, ctx, error):
        """
        Serves as the classifier. It will classify the error and send it to the
        appropriate handler.
        """
        await UncaughtLogger(self.bot).uncaught(ctx, error)
