import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import toml
import yaml


class ConfigType(Enum):
	"""
	This class has project configuration types.
	"""

	TOML = 0
	YAML = 1
	JSON = 2


@dataclass
class UserbotConfig:
	"""
	This class describes an userbot configuration.
	"""

	API_ID: int
	API_HASH: str
	PHONE: str


@dataclass
class BotConfig:
	"""
	This class describes a tg bot configuration.
	"""

	TOKEN: str


@dataclass
class Config:
	"""
	This class describes a configuration.
	"""

	USERBOT: UserbotConfig
	BOT: BotConfig
	LINKS: list = field(default_factory=list)
	DETECTED_PHRASES: list = field(default_factory=list)


class ConfigReader:
	"""
	This class describes a project configuration reader.
	"""

	def __init__(self, config_file: str, configtype: ConfigType = ConfigType.TOML):
		"""
		Constructs a new instance.

		:param		config_file:  The configuration file
		:type		config_file:  str
		:param		configtype:	  The configtype
		:type		configtype:	  ConfigType
		"""
		self.config_file = Path(config_file)
		self.configtype = configtype

	def load_data(self) -> dict:
		"""
		Loads a data from configuration.

		:returns:	configuration dictionary
		:rtype:		dict
		"""
		with open(self.config_file, "r") as fh:
			if self.configtype == ConfigType.YAML:
				data = yaml.load(fh, Loader=yaml.FullLoader)
			elif self.configtype == ConfigType.TOML:
				data = toml.load(fh)
			elif self.configtype == ConfigType.JSON:
				data = json.load(fh)

		userbot = data.get("userbot")
		bot = data.get("bot")

		return Config(
			USERBOT=UserbotConfig(
				API_ID=userbot.get("API_ID"),
				API_HASH=userbot.get("API_HASH"),
				PHONE=userbot.get("PHONE"),
			),
			BOT=BotConfig(TOKEN=bot.get("TOKEN")),
			LINKS=data.get("chats").get("LINKS"),
			DETECTED_PHRASES=data.get("detect").get("PHRASES"),
		)
