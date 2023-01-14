from flask import Flask, jsonify, make_response, request, session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, create_engine, func, desc
from flask_cors import CORS, cross_origin
from functools import wraps
import jwt
import datetime
import secrets

secrets.token_hex(16)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'introduce_one'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://unidb:root1root!@uni.mysql.database.azure.com:3306/discussion_forum"
#db = engine.connect()
#db = SQLAlchemy(app, engine_options={"ssl": {"ssl_ca": "DigiCertGlobalRootCA.crt.pem"}})
db = SQLAlchemy(app)

#cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class Notifications(db.Model):
    notification_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Date, nullable=False)

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(50))
    last_notification_id = db.Column(db.Integer, db.ForeignKey('notifications.notification_id'), nullable=False)

class Tags(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), nullable=False)

class Preferences(db.Model):
    preference_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), nullable=False)

class Discussions(db.Model):
    discussion_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    discussion_id = db.Column(db.Integer, db.ForeignKey('discussions.discussion_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    text = db.Column(db.String(500), nullable=False)

class Blacklisttoken(db.Model):
    token_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

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
           #(request.headers)
           token = request.headers['x-access-tokens'][7:]
       if not token:
           return make_response('missing token', 401,{'message': 'a valid token is missing'})
       cutoff = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
       Blacklisttoken.query.filter(Blacklisttoken.blacklisted_on <= cutoff).delete()
       db.session.commit()
       check_token = Blacklisttoken.query.filter_by(token=token).first()
       if check_token:
           return make_response('blacklisted token', 401,{'message': 'token is blacklisted'})
       try:
           #print(token)
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = Users.query.filter_by(user_id=data['user_id']).first()
       except Exception as e:
           print(e)
           return make_response('invalid token', 401,{'message': 'token is invalid'})
       return f(current_user, *args, **kwargs)
   return decorator


@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization
    #print(auth)
    if not auth or not auth.username or not auth.password:
        return make_response('missing credentials', 401, {'Authentication': 'missing username and/or password'})
    try:
        user = Users.query.filter_by(username=auth.username).first()
        if check_password_hash(user.password, auth.password):
           data = {}
           token = jwt.encode({'user_id' : user.user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=50)}, app.config['SECRET_KEY'], "HS256")
           data['token'] = token
           data['username'] = user.username
           data['user_id'] = user.user_id
           data['email'] = user.mail
           data['name'] = user.name
           data['last_notification_id'] = user.last_notification_id
           session['username'] = user.username
           return jsonify(data)
    except:
        return make_response('could not verify', 401, {'Authentication': 'user has not been found'})
    return make_response('wrong password',  401, {'Authentication': '"login required'})

@app.route('/signup', methods=['POST'])
def signup_post():
    user = request.get_json()
    username = user['username']
    mail = user['email']
    name = user['name']
    password = user['password']
    #print(user)
    user = Users.query.filter_by(mail=mail).first()
    if user:
        return jsonify({'message': 'user already exist'})

    last_not_id = Notifications.query.order_by(desc(Notifications.notification_id)).first()
    #print(last_not_id)
    new_user = Users(username=username, mail=mail, name=name, password=generate_password_hash(password, method='sha256'), last_notification_id=last_not_id.notification_id)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'successfull signup'})

@app.route('/logout')
@token_required
def logout():
    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms=["HS256"])
        if not isinstance(resp, str):
            # mark the token as blacklisted
            blacklist_token = Blacklisttoken(token=auth_token, blacklisted_on=datetime.datetime.now())
            try:
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                session.pop('username', None)
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403

@app.route("/notifications/<notification_id>", methods=['GET'])
@cross_origin()
@token_required
def get_notifications(notification_id):
    ref_notification = Notifications.query.filter_by(notification_id=notification_id).first()
    ref_date = ref_notification.date
    notifications = Notifications.query.filter(Notifications.date > ref_date).all()
    result = []
    for notification in notifications:
        data = {}
        data['notification_id'] = notification.notification_id
        data['text'] = notification.text
        data['date'] = notification.date
        result.append(data)
    return jsonify(result)

@app.route("/tags", methods=['GET'])
@cross_origin()
def get_tags():
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
        return make_response('not found', 404, {'Tag': 'tag not found'})
    result = {}
    result['tag_id'] = tag.tag_id
    result['tag_name'] = tag.tag_name
    return jsonify(result)

@app.route("/preferences", methods=['GET'])
@cross_origin()
@token_required
def get_preferences(current_user):
    preferences = Preferences.query.filter_by(user_id=current_user.user_id).all()
    result = []
    for preference in preferences:
        preference_data = {}
        preference_data['preference_id'] = preference.preference_id
        preference_data['tag_id'] = preference.tag_id
        tag = Tags.query.filter_by(tag_id=preference.tag_id).first()
        preference_data['tag_name'] = tag.tag_name
        result.append(preference_data)
    return jsonify(result)

@app.route("/preferences", methods=['POST'])
@cross_origin()
@token_required
def post_preference(current_user):
    preference = request.get_json()
    new_preference = Preferences(
        user_id=current_user.user_id,
        tag_id=preference['tag_id']
    )
    db.session.add(new_preference)
    db.session.commit()
    db.session.refresh(new_preference)

    result = {}
    result['preference_id'] = new_preference.preference_id
    result['user_id'] = new_preference.user_id
    result['tag_id'] = new_preference.tag_id
    tag = Tags.query.filter_by(tag_id=preference.tag_id).first()
    result['tag_name'] = tag.tag_name

    return jsonify(result)

@app.route("/discussions/<tag_id>", methods=['GET'])
@cross_origin()
def get_discussionlist_by_tag(tag_id):
    #return list of discussion by tagid
    discussions = Discussions.query.filter_by(tag_id=tag_id).all()
    result = []
    for discussion in discussions:
        discussion_data = {}
        discussion_data['discussion_id'] = discussion.discussion_id
        discussion_data['user_id'] = discussion.user_id
        user = Users.query.filter_by(user_id=discussion.user_id).first()
        discussion_data['username'] = user.username
        discussion_data['tag_id'] = discussion.tag_id
        discussion_data['title'] = discussion.title
        discussion_data['description'] = discussion.description
        result.append(discussion_data)
    return jsonify(result)

@app.route("/discussion/<discussion_id>", methods=['GET'])
@cross_origin()
def get_discussion_by_id(discussion_id):
    #get discussion by id
    discussion = Discussions.query.filter_by(discussion_id=discussion_id).first()
    if not discussion:
        return make_response('not found', 404, {'Discussion': 'discussion not found'})
    result = {}
    result['discussion_id'] = discussion.discussion_id
    result['user_id'] = discussion.user_id
    user = Users.query.filter_by(user_id=discussion.user_id).first()
    result['username'] = user.username
    result['tag_id'] = discussion.tag_id
    result['title'] = discussion.title
    result['description'] = discussion.description
    result['comments'] = []

    comments = Comments.query.filter_by(discussion_id=discussion_id).order_by(asc(Comments.date)).all()
    for comment in comments:
        comment_data = {}
        comment_data['comment_id'] = comment.comment_id
        comment_data['user_id'] = comment.user_id
        user = Users.query.filter_by(user_id=comment.user_id).first()
        comment_data['username'] = user.username
        comment_data['discussion_id'] = comment.discussion_id
        date = datetime.datetime.strptime(comment.date, "%Y-%M-%D")
        comment_data['date'] = "{}/{}/{}".format(date.month, date.day,date.year)
        comment_data['text'] = comment.text
        result['comments'].append(comment_data)

    return jsonify(result)

@app.route("/discussions", methods=['POST'])
@cross_origin()
@token_required
def post_discussion(current_user):
    #create new discussion, if tag does not exist, it will be created
    discussion = request.get_json()
    #print(discussion)
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
        user_id=current_user.user_id,
        tag_id=tag.tag_id,
        title=discussion['title'],
        description=discussion['description']
    )
    db.session.add(new_discussion)
    db.session.commit()
    db.session.refresh(new_discussion)

    result = {}
    result['discussion_id'] = new_discussion.discussion_id
    result['user_id'] = new_discussion.user_id
    user = Users.query.filter_by(user_id=new_discussion.user_id).first()
    result['username'] = user.username
    result['tag_id'] = new_discussion.tag_id
    result['title'] = new_discussion.title
    result['description'] = new_discussion.description
    print(result)
    return jsonify(result)

@app.route("/discussion/<discussion_id>", methods=['DELETE'])
@cross_origin()
@token_required
def delete_discussion(current_user, discussion_id):
    discussion = Discussions.query.filter_by(discussion_id=discussion_id).first()
    if not discussion:
        return make_response('not found', 404, {'Discussion': 'discussion not found'})
    if discussion.user_id != current_user.user_id:
        return make_response('Delete prohibited', 401, {'Discussion': 'you are not allowed to delete this'})
    db.session.delete(discussion)
    db.session.commit()
    return jsonify({'message': 'successfull delete'})

@app.route("/discussion/<discussion_id>", methods=['POST'])
@cross_origin()
@token_required
def post_comment(current_user, discussion_id):
    #add new comment to discussion
    comment = request.get_json()
    print(comment['date'])
    date = datetime.datetime.strptime(comment['date'], "%M/%d/%Y")
    new_comment = Comments(
        user_id=current_user.user_id, #comment['user_id'],
        discussion_id=discussion_id, #comment['discussion_id'],
        date=datetime.date(date.year, date.month, date.day),
        text=comment['text']
    )
    db.session.add(new_comment)
    db.session.commit()
    db.session.refresh(new_comment)
    result = {}
    result['comment_id'] = new_comment.comment_id
    result['user_id'] = new_comment.user_id
    user = Users.query.filter_by(user_id=new_comment.user_id).first()
    result['username'] = user.username
    result['discussion_id'] = new_comment.discussion_id
    result['date'] = new_comment.date
    result['text'] = new_comment.text
    return jsonify(result)

@app.route("/comment/<comment_id>", methods=['DELETE'])
@cross_origin()
@token_required
def delete_comment(current_user, comment_id):
    comment = Comments.query.filter_by(comment_id=comment_id).first()
    if not comment:
        return make_response('Comment', 404, {'Comment': 'comment not found'})
    if comment.user_id != current_user.user_id:
        return make_response('Delete prohibited', 401, {'Discussion': 'you are not allowed to delete this'})
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'successfull delete'})

if __name__ == '__main__':
    app.run(debug=True)
