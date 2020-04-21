from aiohttp.client import ClientSession


class _Requester:
    def __init__(self, bot, coroutine):
        self.bot = bot
        self.coroutine = coroutine

    async def __call__(self, *args, **kwargs):
        return await self.coroutine(*args, **kwargs)


class Bot:
    TELEGRAM_API_URL = 'https://api.telegram.org/bot'
    TELEGRAM_DOWNLOAD_FILES_URL = 'https://api.telegram.org/file/bot'

    def __init__(self, token):
        self.token = token
        self.api_url = Bot.TELEGRAM_API_URL + self.token
        self.api_file_url = Bot.TELEGRAM_DOWNLOAD_FILES_URL + self.token

    async def get_method(self, method, params: dict = None):
        if params is None:
            params = {}
        async with ClientSession() as session:
            async with session.request('POST', self.api_url + '/' + method, params=params) as resp:
                resp.raise_for_status()
                return await resp.json()

    def __getattr__(self, item):
        return _Requester(self, self.get_method(item))

