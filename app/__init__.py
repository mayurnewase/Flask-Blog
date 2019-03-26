from flask import Flask
from config import Config

app_instance = Flask(__name__)
app_instance.config.from_object(Config)

from app import routes

