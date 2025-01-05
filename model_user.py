"""Database Model for User"""
# pylint: disable=broad-exception-caught
# pylint: disable=broad-exception-raised
from datetime import datetime, timedelta, timezone
import json
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from config import app, db
from helper import response_json, response_none

class UserModel(db.Model):
    """Database model for user"""
    __tablename__ = "cafe_user"

    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, username, password):
        self.username = str(username)
        self.password = str(password)

    def __repr__(self):
        """Object representation as JSON string"""
        return json.dumps(self.format_object())

    def format_object(self):
        """Object formatting"""
        return {"username": self.username}

    @staticmethod
    def login_match(u: str, p: str) -> bool:
        """Check if username and password is matched"""
        user = UserModel.query.filter_by(username=u).first()
        return bool(user and check_password_hash(user.password, p))

    @staticmethod
    def generate_token(u: str, p: str):
        """Generate token for authentication"""
        if UserModel.login_match(u, p):
            exp = datetime.now(tz=timezone.utc) + timedelta(minutes=app.config["AUTH_EXP_TIME"])
            token = jwt.encode({"exp": exp}, app.config["AUTH_SECRET_KEY"], algorithm="HS256")
            return {"token": token}
        return response_json({"message": "Wrong username and/or password."}, 401)

    @staticmethod
    def decode_token(bearer):
        """Authenticate the token"""
        if bearer is not None:
            token = str(bearer)
            try:
                if token.startswith("Bearer "):
                    token = token.replace("Bearer ", "")
                    return jwt.decode(token, app.config["AUTH_SECRET_KEY"], algorithms=["HS256"])
                raise Exception
            except Exception:
                return response_json({"message": "Invalid token."}, 401)
        return response_json({"message": "Login is required to access this resource."}, 401)

    @staticmethod
    def username_unique(u: str) -> bool:
        """Check for unique username"""
        return UserModel.query.filter_by(username=u).count() > 0

    @staticmethod
    def create(payload):
        """Create new user"""
        if UserModel.username_unique(payload["username"]):
            return response_json({"message": "User name has been used."}, 409)
        try:
            user_to_create = UserModel(
                payload["username"], generate_password_hash(payload["password"])
            )
            db.session.add(user_to_create)
            db.session.commit()
            return response_none(201)
        except Exception as e:
            db.session.rollback()
            raise e
