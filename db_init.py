"""Create Database File"""
from model_menu import db as db_menu
from model_user import db as db_user, UserModel

db_menu.drop_all()
db_user.drop_all()

db_menu.create_all()
db_user.create_all()

create_user_init = UserModel.create({
    "username": "admin",
    "password": "admin"
})
print(create_user_init.status)
