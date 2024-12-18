from telethon import TelegramClient


def create_userbot(config) -> TelegramClient:
	userbot = TelegramClient(
		"userbot", api_id=config.USERBOT.API_ID, api_hash=config.USERBOT.API_HASH
	)
	return userbot
