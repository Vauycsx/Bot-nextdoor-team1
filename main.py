import os
print("BOT_TOKEN:", os.getenv("BOT_TOKEN"))
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
print("WEBHOOK_URL:", os.getenv("WEBHOOK_URL"))

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
from db import init_db
from handlers import router

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def on_startup():
    await init_db()
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()


def main():
    app = web.Application()
    # setup routes, etc.
    web.run_app(app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()
