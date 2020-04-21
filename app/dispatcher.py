from telebot.types import Update


class Handler:
    def __init__(self, coroutine):
        self.coroutine = coroutine

    def is_valid(self, update: Update) -> bool:
        return False

    async def __call__(self, update):
        return await self.coroutine(update)


class CommandHandler(Handler):
    def __init__(self, command: str, coroutine):
        super(CommandHandler, self).__init__(coroutine)
        self._command = command

    def is_valid(self, update: Update) -> bool:
        return isinstance(update.message.text, str) and update.message.text.startswith('/' + self._command)


class Dispatcher:
    def __init__(self, bot):
        self._handlers = []
        self.bot = bot

    async def handle_update(self, update: Update):
        for handle in self._handlers:
            if handle.is_valid(update):
                update.bot = self.bot
                await handle(update)

    def register_handler(self, handler):
        self._handlers.append(handler)
