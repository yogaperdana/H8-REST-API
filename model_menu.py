"""Database Model for Menu"""
# pylint: disable=broad-exception-caught
import json
from flask import Response
from flask_restx import fields
from flask_sqlalchemy import SQLAlchemy
from config import app

db = SQLAlchemy(app)
app.app_context().push()

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
            "id_menu": fields.Integer(
                description="ID of the menu"
            ),
            "name": fields.String(
                required=True,
                description="Name of the menu",
                help="Name cannot be blank"
            ),
            "price": fields.Integer(
                required=True,
                description="Price of the menu",
                help="Price cannot be blank and must be in integer/number"
            ),
            "variations": fields.List(
                fields.String(),
                required=True,
                description="Variation(s) of the menu",
                help="Variation(s) cannot be blank"
            ),
            "category": fields.String(
                required=True,
                description="Category of the menu",
                help="Category cannot be blank"
            )
        }
    }

    def __init__(self, name, price, variations, category):
        self.name = str(name)
        self.price = int(price)
        self.variations = str(variations)
        self.category = str(category)

    def __repr__(self):
        """Object representation as JSON"""
        return json.dumps(self.json())

    def json(self):
        """Format object to JSON"""
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
        return [MenuModel.json(menu) for menu in MenuModel.query.all()]

    @staticmethod
    def get_by_id(id_menu):
        """Get single menu by id"""
        menu_to_select = MenuModel.query.get(id_menu)
        if menu_to_select:
            return MenuModel.json(menu_to_select)
        return Response(response=None, status=404, content_type="application/json")

    @staticmethod
    def create(payload):
        """Add new menu"""
        if MenuModel.check_unique_name(payload["name"]):
            return Response(response=json.dumps({
                "message": "The name has already been used. Please use another."
            }), status=409, content_type="application/json")
        try:
            menu_to_create = MenuModel(
                payload["name"], payload["price"], payload["variations"], payload["category"]
            )
            db.session.add(menu_to_create)
            db.session.commit()
            response = Response(status=201, content_type="application/json")
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
            return Response(status=404, content_type="application/json")
        name_changed = payload["name"] != menu_to_update.name
        name_used = MenuModel.check_unique_name(payload["name"])
        if name_changed and name_used:
            return Response(response=json.dumps({
                "message": "The name has already been used. Please use another."
            }), status=409, content_type="application/json")
        try:
            payload_format = MenuModel(
                payload["name"], payload["price"], payload["variations"], payload["category"]
            )
            menu_to_update.name = payload_format.name
            menu_to_update.price = payload_format.price
            menu_to_update.variations = payload_format.variations
            menu_to_update.category = payload_format.category
            db.session.commit()
            response = Response(status=204, content_type="application/json")
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
            return Response(status=404, content_type="application/json")
        try:
            db.session.delete(menu_to_delete)
            db.session.commit()
            return Response(status=204, content_type="application/json")
        except Exception as e:
            db.session.rollback()
            raise e
