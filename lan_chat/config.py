from dotenv import load_dotenv
import os

env = load_dotenv(dotenv_path=".env")

class AppConfig:
	SECRET_KEY = os.getenv('SECRET_KEY')
	DEBUG = os.getenv('DEBUG')
	SERVER = os.getenv('SERVER')
	PORT = os.getenv('PORT')
	# SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')