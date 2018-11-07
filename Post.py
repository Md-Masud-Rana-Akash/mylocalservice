from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql://root:@localhost/found')

db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    found = db.Column(db.String(191))
    place = db.Column(db.String(191))
    details = db.Column(db.Text)
    image = db.Column(db.String(191))
    lat = db.Column(db.String(191))
    lng = db.Column(db.String(191))
    contact = db.Column(db.String(191))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % self.id
