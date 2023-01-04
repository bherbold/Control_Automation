from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Prices(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(Prices, '/')

if __name__ == '__main__':
    app.run(debug=True)