"""Main Application"""
from flask import Flask, jsonify, Response
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app=app, doc="/docs/", version="1.0", title="FlaskCafe",
          description="Flask Cafe Operations Management")
api = api.namespace("menu", description="Flask Cafe's Menu Operations")

menu_model = api.model(
    "Menu Model",
    {
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
)

menu = [
    {
        "id_menu": 1,
        "name": "Americano",
        "price": 10000,
        "variations": ["Hot", "Ice"],
        "category": "drink"
    },
    {
        "id_menu": 2,
        "name": "Crossiant",
        "price": 5000,
        "variations": ["Butter", "Chocolate"],
        "category": "snack"
    }
]

def valid_menu(menu_object):
    """Check for valid menu object"""
    return {"name", "price", "variations", "category"} <= set(menu_object)

@api.route("/")
class MenuRoot(Resource):
    """Menu root route"""

    @api.doc(responses={
        200: "OK (Success)",
        500: "Internal Server Error (Failed)"
    })
    def get(self):
        """Returns list of menu"""
        return jsonify(menu)

    @api.doc(responses={
        201: "Created (Success)",
        400: "Invalid Argument (Failed)",
        415: "Unsupported Media Type (Failed)",
        500: "Internal Server Error (Failed)"
    })
    @api.expect(menu_model, validate=True)
    def post(self):
        """Add new menu"""
        if valid_menu(api.payload):
            new_menu = {
                "id_menu": menu[-1]["id_menu"] + 1 if len(menu) > 0 else 0,
                "name": api.payload["name"],
                "price": api.payload["price"],
                "variations": api.payload["variations"],
                "category": api.payload["category"]
            }
            menu.append(new_menu)
            response = Response(status=201, content_type="application/json")
            response.location = new_menu['id_menu']
            response.autocorrect_location_header = True
            return response
        return api.abort(400, content_type="application/json")

@api.route("/<int:id_menu>")
class MenuById(Resource):
    """Menu route by id"""

    def find_item(self, id_menu):
        """Find matched item from the id"""
        return next((b for b in menu if b["id_menu"] == id_menu), None)

    @api.doc(responses={
        200: "OK (Success)",
        400: "Invalid Argument (Failed)",
        404: "Not Found (Failed)",
        500: "Internal Server Error (Failed)"
    }, params={"id_menu": "Specify the id associated with the menu to view"})
    def get(self, id_menu):
        """Returns single menu by id"""
        match = self.find_item(id_menu)
        return match if match else Response(status=404, content_type="application/json")

    @api.doc(responses={
        204: "No Content (Success)",
        400: "Invalid Argument (Failed)",
        404: "Not Found (Failed)",
        500: "Internal Server Error (Failed)"
    }, params={"id_menu": "Specify the id associated with the menu to update"})
    @api.expect(menu_model, validate=True)
    def put(self, id_menu):
        """Update single menu by id"""
        match = self.find_item(id_menu)
        if match is not None:
            if valid_menu(api.payload):
                updated_menu = {
                    "id_menu": id_menu,
                    "name": api.payload["name"],
                    "price": api.payload["price"],
                    "variations": api.payload["variations"],
                    "category": api.payload["category"]
                }
                match.update(updated_menu)
                response = Response(
                    status=204, content_type="application/json")
                response.location = updated_menu['id_menu']
                response.autocorrect_location_header = True
                return response
            return api.abort(response=id_menu, status=400, content_type="application/json")
        return Response(status=404, content_type="application/json")

    @api.doc(responses={
        204: "No Content (Success)",
        400: "Invalid Argument (Failed)",
        404: "Not Found (Failed)",
        500: "Internal Server Error (Failed)"
    }, params={"id_menu": "Specify the id associated with the menu to delete"})
    def delete(self, id_menu):
        """Delete single menu by id"""
        global menu  # pylint: disable=global-statement
        match = self.find_item(id_menu)
        if match is not None:
            menu = list(filter(lambda b: b["id_menu"] != id_menu, menu))
            return Response(status=204, content_type="application/json")
        return Response(status=404, content_type="application/json")

@app.errorhandler(404)
def resource_not_found(error):  # pylint: disable=unused-argument
    """Return error message in JSON format if the requested resource was not found"""
    return Response(status=404, content_type="application/json")

if __name__ == "__main__":
    app.run(debug=True)
