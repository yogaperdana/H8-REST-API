"""Configuration"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["AUTH_EXP_TIME"] = 5
app.config["AUTH_SECRET_KEY"] = "77add1d5f41223d5582fca736a5cb335"

db = SQLAlchemy(app)
app.app_context().push()
