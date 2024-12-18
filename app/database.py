import sqlite3


class Database:
	def __init__(self, db_file: str = "users.db"):
		self.conn = sqlite3.connect(db_file)
		self.cursor = self.conn.cursor()
		self.create_table()

	def create_table(self):
		self.cursor.execute(
			"""
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY,
	user_id INTEGER UNIQUE,
	first_name TEXT
)
"""
		)

	def add_user(self, user_id: int, first_name: str):
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

	def get_all_users(self):
		self.cursor.execute("SELECT user_id FROM users")
		return [row[0] for row in self.cursor.fetchall()]

	def close(self):
		self.conn.close()
