import sqlite3
from sqlite3 import Error
from datetime import datetime
import time

# db filename
DB = "chat.db"

class Database:
	"""
	connects, writes and reads from a local sqlite db
	"""
	def __init__(self):
		"""
		setup db connection
		"""
		self.conn = None
		try:
			self.conn = sqlite3.connect(DB, check_same_thread=False)
		except Error as e:
			print(e)

		self.cursor = self.conn.cursor()
		self._create_tables()


	def __del__(self):
		"""
		calls the close function if program ends unexpectedly
		"""
		self.close()


	def close(self):
		"""
		closes db connection
		:return: None
		"""
		self.conn.close()


	def _create_tables(self):
		"""
		creates db tables if they don't exist
		:return: None
		"""
		self.cursor = self.conn.cursor()
		query = f"""CREATE TABLE IF NOT EXISTS ChatRooms (id INTEGER PRIMARY KEY AUTOINCREMENT, room_name TEXT);"""
		self.cursor.execute(query)

		query = f"""INSERT INTO ChatRooms (room_name) SELECT ('Default') WHERE NOT EXISTS (SELECT * FROM ChatRooms);"""
		self.cursor.execute(query)

		query = f"""CREATE TABLE IF NOT EXISTS Messages 
					(id INTEGER PRIMARY KEY AUTOINCREMENT, message_content TEXT, message_created Date, user_name TEXT, room_id INTEGER, CONSTRAINT fk_chatroom FOREIGN KEY (room_id) REFERENCES ChatRooms(id));"""
		self.cursor.execute(query)

		# commit new tables to db before closing cursor
		self.conn.commit()
		self.cursor.close()


	def insert_chat_room(self, room_name):
		"""
		adds a new chat room to the ChatRooms table
		:param: room_name: str
		:return: None
		"""
		self.cursor = self.conn.cursor()
		query = f"""INSERT INTO ChatRooms (room_name) VALUES({room_name})"""

		# execute and commit query
		self.cursor.execute(query)
		self.conn.commit()
		self.cursor.close()


	def insert_new_message(self, content, user, room=1):
		"""
		adds a new message to the Messages table
		:param: content: str
		:param: user: str
		:param: room: int 1
		:return: None
		"""
		self.cursor = self.conn.cursor()
		create_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
		query = f"""INSERT INTO Messages (message_content, message_created, user_name, room_id) VALUES(?, ?, ?, ?)"""

		# execute and commit query
		self.cursor.execute(query, (content, create_time, user, room))
		self.conn.commit()
		self.cursor.close()


	def get_default_room(self):
		"""
		gets the default room
		:return: list[]
		"""
		self.cursor = self.conn.cursor()
		self.cursor.execute("SELECT * FROM ChatRooms WHERE id = 1;")
		result = self.cursor.fetchall()
		self.cursor.close()
		return result


	def get_all_rooms(self):
		"""
		gets all rooms
		:return: list[dict]
		"""
		self.cursor = self.conn.cursor()
		self.cursor.execute("SELECT * FROM ChatRooms ORDER BY id;")
		result = self.cursor.fetchall()
		self.cursor.close()

		results = []

		for row in result:
			results.append({"id": row[0], "name": row[1]})

		return jsonify(results)


	def get_all_messages(self, limit=100, user=None):
		"""
		gets all messages with a set limit
		:param: limit: 100
		:param: user: str
		:return: list[dict]
		"""

		# perform query logic
		self.cursor = self.conn.cursor()

		if not user:
			query = f"SELECT * FROM Messages ORDER BY message_created ASC LIMIT ?;"
			self.cursor.execute(query, (limit,))
		else:
			query = f"SELECT * FROM Messages WHERE user_name = ? ORDER BY message_created ASC LIMIT ?;"
			self.cursor.execute(query, (user, limit))

		result = self.cursor.fetchall()
		self.cursor.close()

		results = []

		for row in result:
			results.append({"id": row[0], "content": row[1], "created": row[2], "user": row[3], "room": row[4]})

		return results


	def get_messages_by_user(self, user, limit=100):
		"""
		gets messages sent by a user
		:param: user: str
		:param: limit: 100
		:return: list[dict]
		"""
		return self.get_all_messages(limit=limit, user=user)
