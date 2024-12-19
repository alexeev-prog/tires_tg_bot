import sqlite3


class Database:
	"""
	This class describes a database.
	"""

	def __init__(self, db_file: str = "users.db"):
		"""
		Constructs a new instance.

		:param		db_file:  The database file
		:type		db_file:  str
		"""
		self.conn = sqlite3.connect(db_file)
		self.cursor = self.conn.cursor()
		self.create_table()

	def create_table(self):
		"""
		Creates a table.
		"""
		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY,
	user_id INTEGER UNIQUE,
	first_name TEXT
)
"""
		)

	def add_user(self, user_id: int, first_name: str) -> bool:
		"""
		Adds an user.

		:param		user_id:	 The user identifier
		:type		user_id:	 int
		:param		first_name:	 The first name
		:type		first_name:	 str

		:returns:	True if created else False
		:rtype:		bool
		"""
		try:
			self.cursor.execute(
				"INSERT INTO users (user_id, first_name) VALUES (?, ?)",
				(user_id, first_name),
			)
			self.conn.commit()
			return True
		except sqlite3.IntegrityError as ex:
			print(f"Exception: {ex}")
			return False

	def get_all_users(self) -> list:
		"""
		Gets all users.

		:returns:	All users.
		:rtype:		list
		"""
		self.cursor.execute("SELECT user_id FROM users")
		return [row[0] for row in self.cursor.fetchall()]

	def close(self):
		"""
		Close connection
		"""
		self.conn.close()
