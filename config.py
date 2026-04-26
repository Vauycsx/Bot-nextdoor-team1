import os
import sys

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

DATABASE_URL = os.getenv("DATABASE_URL")

WEBHOOK_PATH = "/webhook"

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL is not set")

ADMIN_ID = int(os.getenv("ADMIN_ID", "6752278578"))
