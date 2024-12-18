# import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.database import Database


async def broadcast_message(bot: Bot, db: Database, message: str):
	users = db.get_all_users()

	for user_id in users:
		try:
			await bot.send_message(user_id, message)
			print(f'Message "{message}" sent to {user_id}')
		except Exception as ex:
			print(f"Error sending message to {user_id}: {ex}")


def create_bot(token: str):
	db = Database()
	bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
	dp = Dispatcher()

	return bot, dp, db
