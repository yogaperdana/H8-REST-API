"""Main Application"""
from flask import Response
from flask_restx import Api, Resource
from config import app
from helper import doc_responses
from model_menu import MenuModel

api = Api(
    app=app, doc="/docs/", version="1.1", title="FlaskCafe",
    description="Flask Cafe Operations Management"
)
api = api.namespace("menu", description="Flask Cafe's Menu Operations")
api_model_menu = api.model(**MenuModel.api_model)

@api.route("/")
class MenuRoot(Resource):
    """Menu root route"""

    @api.doc(responses=doc_responses([200, 500]))
    def get(self):
        """Returns list of menu"""
        return MenuModel.get_all()

    @api.doc(responses=doc_responses([201, 400, 409, 415, 500]))
    @api.expect(api_model_menu, validate=True)
    def post(self):
        """Add new menu"""
        return MenuModel.create(api.payload)

@api.route("/<int:id_menu>")
class MenuById(Resource):
    """Menu route by id"""

    @api.doc(responses=doc_responses([200, 400, 404, 500]),
             params={"id_menu": "Specify the id associated with the menu"})
    def get(self, id_menu):
        """Returns single menu by id"""
        return MenuModel.get_by_id(id_menu)

    @api.doc(responses=doc_responses([204, 400, 404, 409, 500]),
             params={"id_menu": "Specify the id associated with the menu"})
    @api.expect(api_model_menu, validate=True)
    def put(self, id_menu):
        """Update single menu by id"""
        return MenuModel.update(id_menu, api.payload)

    @api.doc(responses=doc_responses([204, 400, 404, 500]),
             params={"id_menu": "Specify the id associated with the menu"})
    def delete(self, id_menu):
        """Delete single menu by id"""
        return MenuModel.delete(id_menu)

@app.errorhandler(404)
def resource_not_found(error): # pylint: disable=unused-argument
    """Return empty body response if the requested resource was not found"""
    return Response(status=404, content_type="application/json")

if __name__ == "__main__":
    app.run(debug=True)
