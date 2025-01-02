"""Create Database File"""
from model_menu import db
db.drop_all()
db.create_all()
