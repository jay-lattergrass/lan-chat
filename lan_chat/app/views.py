from flask import Flask, render_template, redirect, request, session, Blueprint, url_for, jsonify
from .database import Database


db = Database()
view = Blueprint("views", __name__)


@view.route("/")
@view.route("/chat")
def chat():
	if "user_name" not in session:
		# redirect to login
		return redirect(url_for("views.login"))

	return render_template("index.html", **{"session": session})


@view.route("/history")
def history():
	if "user_name" not in session:
		# redirect to login
		return redirect(url_for("views.login"))

	# json = get_history()
	json = db.get_messages_by_user(user=session["user_name"])

	return render_template("history.html", **{"json": json})


@view.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		post_data = request.form.to_dict()

		# if no user_name is in session, then create variable
		if "user_name" not in session:
			session["user_name"] = post_data["inputName"].lower()
			return redirect(url_for("views.chat"))
		else:
			return redirect(url_for("views.chat"))

	return render_template("login.html", **{"session": session})


@view.route("/logout")
def logout():
	if "user_name" in session:
		# clear session variables
		session.clear()

	return redirect(url_for("views.login"))


@view.route("/get_default_room")
def get_default_room():
	room = db.get_default_room()
	return jsonify(room)


@view.route("/get_all_messages")
def get_all_messages():
	msgs = db.get_all_messages()
	return jsonify(msgs)


@view.route("/get_user_name")
def get_user_name():
	user = session["user_name"]
	return jsonify({"user_name": user})


@view.route("/get_history")
def get_history():
	msgs = db.get_messages_by_user(user=session["user_name"])
	return jsonify(msgs)
