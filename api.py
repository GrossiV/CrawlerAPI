from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class About(Resource):
    def get(self, url):
        return {'about' : url}

api.add_resource(About, '/<string:url>')

if __name__ == '__main__':
    app.run(debug=False)