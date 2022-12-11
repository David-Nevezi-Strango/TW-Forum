from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)




class ResourceHandler(Resource):
    def get(self):
        return {"Hello":"World!"}

api.add_resource(ResourceHandler, "/")

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
