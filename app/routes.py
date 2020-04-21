from aiohttp import web
from telebot.types import Update

routes = web.RouteTableDef()


@routes.post('/bot_updates')
async def get_updates(request: web.Request):
    update = Update.de_json(request.json())
    await request.app.dispatcher.handle_update(update)
