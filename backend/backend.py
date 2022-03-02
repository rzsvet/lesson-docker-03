import os
import logging
from os import path
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from datetime import datetime

logging.basicConfig(filename='app.log')
DATABASE_FILE = "database.db"
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(DATABASE_FILE)
app.config["SQLALCHEMY_DATABASE_URI"] = (os.environ.get(
    'DATABASE_URI', 'postgresql://postgres:password@127.0.0.1/'))
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@127.0.0.1/"

db = SQLAlchemy(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')


class ApiPost(Resource):
    def get(self):
        return jsonify(posts=[i.serialize for i in Post.query.all()], lenght=Post.query.count())

    def post(self):
        args = parser.parse_args()
        if args.get('title') is not None and args.get('description') is not None:
            db.session.add(Post(request.form.get("title"),
                                request.form.get("description")))
            db.session.commit()
            return {'message': 'successful'}, 201
            # return {'message': 'successful', 'data': args}, 201
            # return args, 201
        else:
            return args, 400


api.add_resource(ApiPost, '/post')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_on': dump_datetime(self.created_on),
            'updated_on': dump_datetime(self.updated_on),
        }

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        # return { 'Title': format(self.title), 'Description': format(self.description) }
        return "<Title: {}>".format(self.title)


@app.route("/", methods=["GET", "POST"])
def post():
    return '<h1>This is backend version of application</h1>'

# @app.route("/post", methods=["GET", "POST"])
# def post():
#     if request.form:
#         data = Post(request.form.get("title"), request.form.get("description"))
#         db.session.add(data)
#         db.session.commit()
#     posts = Post.query.all()
#     return render_template("index.html", posts=posts, mode=os.environ.get('FLASK_ENV', 'development'))


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


def init_db():
    db.create_all()
    db.session.add(Post("Test post number one",
                        "This description for post number one"))
    db.session.add(Post("Test post number two",
                        "This description for post number two"))
    db.session.commit()


if __name__ == "__main__":
    if not path.exists(DATABASE_FILE):
        init_db()
    if (os.environ.get('FLASK_ENV', 'development') == 'development'):
        app.run(host='0.0.0.0', port=(
            os.environ.get('APP_PORT', 8080)), debug=True)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=(
            os.environ.get('APP_PORT', 8080)))


def test_dump_datetime_date():
    test_date = datetime(2022, 2, 14, 17, 12, 55)
    assert dump_datetime(test_date) == ['2022-02-14', '17:12:55']


def test_dump_datetime_none():
    assert dump_datetime(None) is None
