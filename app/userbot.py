from telethon import TelegramClient

from app.config import Config


def create_userbot(config: Config) -> TelegramClient:
	"""
	Creates an userbot.

	:param		config:	 The configuration
	:type		config:	 Config

	:returns:	The telegram client.
	:rtype:		TelegramClient
	"""
	userbot = TelegramClient(
		"userbot", api_id=config.USERBOT.API_ID, api_hash=config.USERBOT.API_HASH
	)
	return userbot
