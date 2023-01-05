from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, create_engine
from flask_cors import CORS, cross_origin
from functools import wraps
#import uuid
import jwt
import datetime
import secrets

secrets.token_hex(16)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'introduce_one'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://unidb:root1root!@uni.mysql.database.azure.com:3306/discussion_forum"# ?ssl=true
#app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"ssl": {"ca": "DigiCertGlobalRootCA.crt.pem"}}
#engine = create_engine("mysql+pymysql://root:root1root!@localhost:3306/discussion_forum",connect_args={"ssl": {"ssl_ca": "DigiCertGlobalRootCA.crt.pem"}})
#{"ssl": {"ssl_ca": "DigiCertGlobalRootCA.crt.pem"}}
#db = engine.connect()
#db = SQLAlchemy(app, engine_options={"ssl": {"ssl_ca": "DigiCertGlobalRootCA.crt.pem"}})
db = SQLAlchemy(app)

#cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50))

class Tags(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), nullable=False)

class Preferences(db.Model):
    preference_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), nullable=False)

class Discussions(db.Model):
    discussion_id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussion.discussion_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    text = db.Column(db.String(500), nullable=False)

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Credentials', 'true')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Application/Json')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,OPTION,POST,DELETE')
#     return response

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = Users.query.filter_by(user_id=data['user_id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
       return f(current_user, *args, **kwargs)
   return decorator

@app.route('/login', methods=['POST'])
def login_user():
   auth = request.authorization
   if not auth or not auth.username or not auth.password:
       return make_response('could not verify', 401, {'Authentication': 'login required"'})
   user = Users.query.filter_by(username=auth.username).first()
   if check_password_hash(user.password, auth.password):
       token = jwt.encode({'user_id' : user.user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=50)}, app.config['SECRET_KEY'], "HS256")
       return jsonify({'token' : token})
   return make_response('could not verify',  401, {'Authentication': '"login required"'})

#@app.route("/", methods=['GET'])
#@app.route("/home", methods=['GET'])
@app.route("/tags", methods=['GET'])
@cross_origin()
def home():
    tags = Tags.query.all()
    result = []
    for tag in tags:
        tag_data = {}
        tag_data['tag_id'] = tag.tag_id
        tag_data['tag_name'] = tag.tag_name
        result.append(tag_data)
    return jsonify(result)

@app.route("/tags/<tag_id>", methods=['GET'])
@cross_origin()
def get_tag_by_id(tag_id):
    tag = Tags.query.filter_by(tag_id=tag_id).first()
    if not tag:
        return jsonify({'message': 'no tag like this'})
    result = {}
    result['tag_id'] = tag.tag_id
    result['tag_name'] = tag.tag_name
    return jsonify(result)

@app.route("/discussions", methods=['POST'])
@cross_origin()
def post_discussion():
    #create new discussion, if tag does not exist, it will be created
    if request.method == 'POST':
        discussion = request.get_json()
        print(discussion)
        tag = Tags.query.filter_by(tag_name=discussion['tag_name']).first()
        if tag is None:
            tag = Tags(
                tag_name=discussion['tag_name']
            )
            db.session.add(tag)
            db.session.commit()
            db.session.refresh(tag)
            #tag = Tags.query.filter_by(tag_name=discussion['tag_name']).first()

        new_discussion = Discussions(
            tag_id=tag.tag_id,
            title=discussion['title'],
            description=discussion['description']
        )
        db.session.add(new_discussion)
        db.session.commit()
        db.session.refresh(new_discussion)

        result = {}
        result['discussion_id'] = new_discussion.discussion_id
        result['tag_id'] = new_discussion.tag_id
        result['title'] = new_discussion.title
        result['description'] = new_discussion.description
        return jsonify(result)#redirect?
#and if new tag?

@app.route("/discussions/<tag_id>", methods=['GET'])
@cross_origin()
def get_discussionlist_by_tag(tag_id):
    #return list of discussion by tagid
    discussions = Discussions.query.filter_by(tag_id=tag_id).all()
    result = []
    for discussion in discussions:
        discussion_data = {}
        discussion_data['discussion_id'] = discussion.discussion_id
        discussion_data['tag_id'] = discussion.tag_id
        discussion_data['title'] = discussion.title
        discussion_data['description'] = discussion.description
        result.append(discussion_data)
    return jsonify(result)

@app.route("/discussion/<discussion_id>", methods=['GET', 'POST'])
@cross_origin()
#@token_required
def get_post_discussion_by_id(discussion_id):
    #add new comment to discussion
    if request.method == 'POST':
        comment = request.get_json()
        new_comment = Comments(
            user_id=comment['user_id'],
            discussion_id=comment['discussion_id'],
            date=comment['date'],
            text=comment['text']
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'message': 'comment created'})#refresh with comment?
    else:
        #get discussion by id
        discussion = Discussions.query.filter_by(discussion_id=discussion_id).first()
        if not discussion:
            return jsonify({'message': 'discussion does not exist'})
        result = {}
        result['discussion_id'] = discussion.discussion_id
        result['tag_id'] = discussion.tag_id
        result['title'] = discussion.title
        result['description'] = discussion.description
        result['comments'] = []

        comments = Comments.query.filter_by(discussion_id=discussion_id).order_by(asc(Comments.date)).all()
        for comment in comments:
            comment_data = {}
            comment_data['comment_id'] = comment.comment_id
            comment_data['user_id'] = comment.user_id
            comment_data['discussion_id'] = comment.discussion_id
            comment_data['date'] = comment.date
            comment_data['text'] = comment.text
            result['comments'].append(comment_data)

        return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
