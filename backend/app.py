from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

discussion_put_args = reqparse.RequestParser()
discussion_put_args.add_argument("title", type=str, help="Title of the discussion is required", required=True)

class Discussion(Resource):
    def get(self, discussion_id):
        #sql
        pass
    def put(self):
        args = discussion_put_args.parse_args()
        discussion = args
        #sql
        return 0

comment_put_args = reqparse.RequestParser()
comment_put_args.add_argument("text", type=str, help="Text of the comment is required", required=True)

class Comment(Resource):
    def get(self, comment_id):
        return {"hello":"there"}
    def put(self, comment_id):
        #request.form
        args = comment_put_args.parse_args()
        print(args)
        #sql
        return args

class Preferences(Resource):
    def get(self, user_id):
        #sql
        return

#class Tags(Resource):

#class User(Resource):


class ResourceHandler(Resource):
    def get(self):
        return {"Hello":"World!"}

api.add_resource(ResourceHandler, "/")
api.add_resource(Discussion, "/discussion")
api.add_resource(Comment, "/comment/<int:comment_id>")

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
