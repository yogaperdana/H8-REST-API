"""Main Application"""
from flask import Response, request
from flask_restx import Api, Resource
from config import app
from helper import doc_responses, response_json, response_none
from model_menu import MenuModel
from model_user import UserModel

api_auth = {
    "token": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Generate token from **POST /auth/login**\n"
            "Authorization format: **Bearer \\<token\\>**"
    }
}
api = Api(
    app=app, doc="/docs/", version="1.2", title="FlaskCafe",
    description="Flask Cafe Operations Management",
    authorizations=api_auth
)
ns_auth = api.namespace("auth", description="User Operations")
ns_menu = api.namespace("menu", description="Menu Operations")
api_model_menu = ns_menu.model(**MenuModel.api_model)

@ns_auth.route("/login")
class AuthRoot(Resource):
    """Root authentication route"""

    @ns_auth.doc(responses=doc_responses([200, 401, 500]))
    @ns_auth.param("username", _in="formData", type=str, required=True)
    @ns_auth.param("password", _in="formData", type=str, required=True)
    def post(self):
        """Login to get the authorization token"""
        auth = request.form
        u = str(auth.get("username"))
        p = str(auth.get("password"))
        if not auth or not u or not p:
            return response_json({"message": "Please provide username and password."}, 401)
        return UserModel.generate_token(u, p)

@ns_menu.route("/")
class MenuRoot(Resource):
    """Root menu route"""

    @ns_menu.doc(
        responses=doc_responses([200, 401, 500]),
        security="token"
    )
    def get(self):
        """Returns list of menu"""
        auth = UserModel.decode_token(request.headers.get("Authorization"))
        if isinstance(auth, Response):
            return auth
        return MenuModel.get_all()

    @ns_menu.doc(
        responses=doc_responses([201, 400, 401, 409, 415, 500]),
        security="token"
    )
    @ns_menu.expect(api_model_menu, validate=True)
    def post(self):
        """Add new menu"""
        auth = UserModel.decode_token(request.headers.get("Authorization"))
        if isinstance(auth, Response):
            return auth
        return MenuModel.create(api.payload)

@ns_menu.route("/<int:id_menu>")
class MenuById(Resource):
    """Menu route by id"""

    param_id_menu = {"id_menu": "Specify the id associated with the menu"}

    @ns_menu.doc(
        responses=doc_responses([200, 400, 401, 404, 500]),
        security="token",
        params=param_id_menu
    )
    def get(self, id_menu):
        """Returns single menu by id"""
        auth = UserModel.decode_token(request.headers.get("Authorization"))
        if isinstance(auth, Response):
            return auth
        return MenuModel.get_by_id(id_menu)

    @ns_menu.doc(
        responses=doc_responses([204, 400, 401, 404, 409, 500]),
        security="token",
        params=param_id_menu
    )
    @ns_menu.expect(api_model_menu, validate=True)
    def put(self, id_menu):
        """Update single menu by id"""
        auth = UserModel.decode_token(request.headers.get("Authorization"))
        if isinstance(auth, Response):
            return auth
        return MenuModel.update(id_menu, api.payload)

    @ns_menu.doc(
        responses=doc_responses([204, 400, 401, 404, 500]),
        security="token",
        params=param_id_menu
    )
    def delete(self, id_menu):
        """Delete single menu by id"""
        auth = UserModel.decode_token(request.headers.get("Authorization"))
        if isinstance(auth, Response):
            return auth
        return MenuModel.delete(id_menu)

@app.errorhandler(404)
def resource_not_found(error):
    """Return empty body response if the requested resource was not found"""
    app.logger.warning(error)
    return response_none(404)

if __name__ == "__main__":
    app.run(debug=True)
