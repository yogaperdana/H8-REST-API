"""Database Model for Menu"""
# pylint: disable=broad-exception-caught
import json
from flask_restx import fields
from config import db
from helper import response_json, response_none

class MenuModel(db.Model):
    """Database model for menu"""
    __tablename__ = "cafe_menu"

    id_menu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    variations = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(64), nullable=False)

    api_model = {
        "name": "Menu Model",
        "model": {
            "name": fields.String(
                required=True,
                description="Name of the menu",
                help="Name cannot be blank",
                default="New Menu"
            ),
            "price": fields.Integer(
                required=True,
                description="Price of the menu",
                help="Price cannot be blank and must be in integer/number",
                default=10000
            ),
            "variations": fields.List(
                fields.String(),
                required=True,
                description="Variation(s) of the menu",
                help="Variation(s) cannot be blank",
                default="[]"
            ),
            "category": fields.String(
                required=True,
                description="Category of the menu",
                help="Category cannot be blank",
                default="food"
            )
        }
    }

    def __init__(self, name, price, variations, category):
        self.name = str(name)
        self.price = int(price)
        self.variations = str(variations)
        self.category = str(category)

    def __repr__(self):
        """Object representation as JSON string"""
        return json.dumps(self.format_object())

    def format_object(self):
        """Object formatting"""
        return {
            "id_menu": self.id_menu,
            "name": self.name,
            "price": self.price,
            "variations": self.variations.strip("[]").replace("'", "").split(", "),
            "category": self.category
        }

    @staticmethod
    def check_unique_name(name):
        """Check for unique menu's name"""
        return MenuModel.query.filter_by(name=name).count() > 0

    @staticmethod
    def get_all():
        """Get all menu"""
        return [MenuModel.format_object(menu) for menu in MenuModel.query.all()]

    @staticmethod
    def get_by_id(id_menu):
        """Get single menu by id"""
        menu_to_select = MenuModel.query.get(id_menu)
        if menu_to_select:
            return MenuModel.format_object(menu_to_select)
        return response_none(404)

    @staticmethod
    def create(payload):
        """Add new menu"""
        if MenuModel.check_unique_name(payload["name"]):
            return response_json(
                {"message": "The name has already been used. Please use another."}, 409
            )
        try:
            menu_to_create = MenuModel(
                payload["name"], payload["price"], payload["variations"], payload["category"]
            )
            db.session.add(menu_to_create)
            db.session.commit()
            response = response_none(201)
            response.location = menu_to_create.id_menu
            response.autocorrect_location_header = True
            return response
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update(id_menu, payload):
        """Update menu"""
        menu_to_update = MenuModel.query.get(id_menu)
        if menu_to_update is None:
            return response_none(404)
        name_changed = payload["name"] != menu_to_update.name
        name_used = MenuModel.check_unique_name(payload["name"])
        if name_changed and name_used:
            return response_json(
                {"message": "The name has already been used. Please use another."}, 409
            )
        try:
            payload_format = MenuModel(
                payload["name"], payload["price"], payload["variations"], payload["category"]
            )
            menu_to_update.name = payload_format.name
            menu_to_update.price = payload_format.price
            menu_to_update.variations = payload_format.variations
            menu_to_update.category = payload_format.category
            db.session.commit()
            response = response_none(204)
            response.location = menu_to_update.id_menu
            response.autocorrect_location_header = True
            return response
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(id_menu):
        """Delete single menu by id"""
        menu_to_delete = MenuModel.query.get(id_menu)
        if menu_to_delete is None:
            return response_none(404)
        try:
            db.session.delete(menu_to_delete)
            db.session.commit()
            return response_none(204)
        except Exception as e:
            db.session.rollback()
            raise e
