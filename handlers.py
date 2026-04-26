from aiogram import Router
from aiogram.types import Message
from config import ADMIN_ID
from db import pool
from keyboards import get_menu

router = Router()

admin_state = {}
last_item = {}


async def get_user(uid):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM users WHERE id=$1", uid)


@router.message()
async def handler(msg: Message):
    uid = msg.from_user.id
    text = msg.text

    user = await get_user(uid)

    # ===== ADMIN INPUT =====
    if uid == ADMIN_ID and uid in admin_state:
        mode = admin_state[uid]

        table = {
            "code": "codes",
            "email": "emails",
            "domain": "domains",
            "access": "accesses",
            "manual": "manuals"
        }[mode]

        async with pool.acquire() as conn:
            await conn.execute(f"INSERT INTO {table} VALUES ($1)", text)

        del admin_state[uid]
        return await msg.answer("✅ добавлено")

    # ===== START =====
    if text == "/start":
        if not user and uid != ADMIN_ID:
            return await msg.answer("🔐 Введи код доступа")

        return await msg.answer(
            "🚀 CRM Online",
            reply_markup=get_menu(uid == ADMIN_ID)
        )

    # ===== AUTH =====
    if not user and uid != ADMIN_ID:
        async with pool.acquire() as conn:
            code = await conn.fetchrow(
                "SELECT * FROM codes WHERE code=$1", text
            )

            if not code:
                return await msg.answer("❌ Неверный код")

            await conn.execute("DELETE FROM codes WHERE code=$1", text)
            await conn.execute(
                "INSERT INTO users (id, role) VALUES ($1, $2)",
                uid, "user"
            )

        return await msg.answer("✅ доступ открыт")

    # ===== PROFILE =====
    if text == "👤 Профиль":
        role = "admin" if uid == ADMIN_ID else user["role"]

        return await msg.answer(
            f"👤 ID: {uid}\n🎭 {role}"
        )

    # ===== EMAIL =====
    if text == "📧 Почта":
        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM emails LIMIT 1")

            if not row:
                return await msg.answer("пусто")

            await conn.execute("DELETE FROM emails WHERE value=$1", row["value"])

        last_item[uid] = row["value"]
        return await msg.answer(row["value"])