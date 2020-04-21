import os

from aiohttp import web

from telebot.types import Update, Message, WebhookInfo

from app import routes
from app.db import init_db
from app.models.user import UserModel, SettingsModel
from app.dispatcher import Dispatcher, CommandHandler
from app.bot import Bot


def send_message(update: Update, text):
    return Message.de_json(update.bot.get_method('sendMessage', params=dict(
        chat_id=update.message.chat.id,
        text=text
    )))


async def hello_msg(update: Update):
    await UserModel.get_or_create({'id': update.message.from_user.id})
    return send_message(update, f'Привет, {update.message.user.username}')


async def set_setting(update: Update):
    user, created = await UserModel.get_or_create({'id': update.message.from_user.id})
    msg: str = update.message.text
    msg_args = msg.split()[1:]
    if len(msg_args) < 2:
        return send_message(update, 'Вы не указали ключ и/или значение')
    key, value = msg_args
    setting, created = await SettingsModel.get_or_create(owner_id=user.id, key=key)
    setting.value = value
    await setting.save()
    return send_message(update, 'Значение записано')


async def get_setting(update: Update):
    user, created = await UserModel.get_or_create({'id': update.message.from_user.id})
    msg: str = update.message.text
    msg_args = msg.split()[1:]
    if len(msg_args) < 2:
        return send_message(update, 'Вы не указали ключ')
    key = msg_args[0]
    setting = await SettingsModel.get_or_none(owner_id=user.id, key=key)
    if setting is None:
        return send_message(update, f'Данного ключа не найдено! Чтобы задать значение напишите:'
                                    f'\n /set_value {key} ЗНАЧЕНИЕ')
    return send_message(update, f'Значение для {key} - {setting.value}')


async def init_app():
    app = web.Application()
    app.add_routes(routes.routes)
    await init_db()
    app.bot = Bot(os.environ.get('BOT_TOKEN', ''))
    app.dispatcher = Dispatcher(app.bot)
    app.dispatcher.register_handler(CommandHandler('start', hello_msg))
    app.dispatcher.register_handler(CommandHandler('set_value', set_setting))
    app.dispatcher.register_handler(CommandHandler('get_value', get_setting))

    wi = WebhookInfo.de_json((await app.bot.get_method('getWebhookInfo'))['result'])
    if wi.url == '':
        await app.bot.get_method('setWebhook', params={'url': os.environ.get('URL', '') + '/bot_updates'})
    return app

if __name__ == '__main__':
    web.run_app(init_app())
