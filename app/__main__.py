import argparse
import asyncio

from aiogram import types
from telethon import events

from app.bot import broadcast_message, create_bot
from app.config import ConfigReader, ConfigType
from app.userbot import create_userbot

config = {}


def load_args():
	"""
	Loads arguments.
	"""
	global config

	PARSER = argparse.ArgumentParser()
	PARSER.add_argument(
		"config", default="config.toml", type=str, help="Path to YAML/TOML/JSON config"
	)
	args = PARSER.parse_args()

	config_reader = ConfigReader(args.config, ConfigType.TOML)
	config = config_reader.load_data()


load_args()

userbot = create_userbot(config)

tgbot = create_bot(config.BOT.TOKEN)
dp = tgbot.dp
bot = tgbot.bot
db = tgbot.db


@dp.message()
async def start(message: types.Message):
	"""
	Any message (echo-bot)

	:param		message:  The message
	:type		message:  types.Message
	"""
	if db.add_user(message.from_user.id, message.from_user.first_name):
		await message.answer("Вы успешно подключились к рассылке!")
	else:
		await message.answer("Вы уже подключены к рассылке!")


@userbot.on(events.NewMessage())
async def message_handler(event):
	"""
	User-bot message handler (phrases)

	:param		event:	The event
	:type		event:	event
	"""
	message_text = event.message.message

	if str(event.chat_id) in config.LINKS:
		if any(
			keyword in message_text.lower().strip()
			for keyword in config.DETECTED_PHRASES
		):
			sender = await event.get_sender()
			date = event.message.date.strftime("%Y-%m-%d %H:%M:%S")
			sender_name = sender.first_name
	
			await broadcast_message(
				bot,
				db,
				f"<b>[{date}] Новое сообщение!</b>\n\n{message_text}\n\n" \
				f"От: <a href='tg://user?id={event.sender_id}'>@{str(sender.username)} ({sender_name})</a>",
			)


async def main():
	"""
	Run userbot and bot
	"""
	print("Start Userbot")
	await userbot.start()
	print("Polling Bot")
	await dp.start_polling(bot)
	print("End.")


if __name__ == "__main__":
	asyncio.run(main())
