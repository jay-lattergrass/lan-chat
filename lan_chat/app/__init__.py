from flask import Flask

def app_create():
	""" Creates the core application """
	# create app and get config
	app = Flask(__name__, instance_relative_config=False, static_url_path="/static", static_folder="static", template_folder="templates")
	app.config.from_object('config.AppConfig')

	with app.app_context():
		# import
		from .views import view

		# register routes
		app.register_blueprint(view, url_prefix="/")

		return app