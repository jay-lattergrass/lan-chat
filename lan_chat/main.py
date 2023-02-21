from flask import Flask
from app import app_create
from app.database import Database
from flask_socketio import SocketIO
from datetime import datetime

app = app_create()
socketio = SocketIO(app)	# used for user communication

# socket event handler
@socketio.on("insert_message")
def handle_message_insert(json, methods=["GET", "POST"]):
	"""
	handles saving new messages
	:param: json
	:param: methods: GET POST
	:return: None
	"""
	data = dict(json)
	if "user" in data:
		db = Database()
		db.insert_new_message(data["content"], data["user"], 1)

	json["created"] = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
	socketio.emit("message_response", json)

# start server
if __name__ == "__main__":
	# run app
	app.run(debug=True)
