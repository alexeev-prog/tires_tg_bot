# import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.database import Database


class TGBot:
	"""
	This class describes a tg bot.
	"""

	def __init__(self, token: str):
		"""
		Constructs a new instance.

		:param		token:	The token
		:type		token:	str
		"""
		self.token = token
		self._db = Database()
		self._bot = Bot(
			token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
		)
		self._dp = Dispatcher()

	@property
	def db(self) -> Database:
		"""
		Get database class instance

		:returns:	database class instance
		:rtype:		Database
		"""
		return self._db

	@property
	def bot(self) -> Bot:
		"""
		Get telegram bot instance

		:returns:	bot class instance
		:rtype:		Bot
		"""
		return self._bot

	@property
	def dp(self) -> Dispatcher:
		"""
		Get dispatcher instance

		:returns:	dispatcher class instance
		:rtype:		Dispatcher
		"""
		return self._dp


async def broadcast_message(bot: Bot, db: Database, message: str):
	"""
	Broadcasts a message.

	:param		bot:	  The bottom
	:type		bot:	  Bot
	:param		db:		  The database
	:type		db:		  Database
	:param		message:  The message
	:type		message:  str
	"""
	users = db.get_all_users()

	for user_id in users:
		try:
			await bot.send_message(user_id, message)
			print(f'Message "{message}" sent to {user_id}')
		except Exception as ex:
			print(f"Error sending message to {user_id}: {ex}")


def create_bot(token: str) -> TGBot:
	"""
	Creates a tg bot and return instance

	:param		token:	The token
	:type		token:	str

	:returns:	TGBot class instance
	:rtype:		TGBot
	"""
	tgbot = TGBot(token)

	return tgbot
