from flask import Flask, jsonify, Response, render_template, request
import sys
import os
import json
import datetime
import time
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://root:@localhost/found')

db = SQLAlchemy(app)
date_format = '%Y-%m-%d %H:%M:%S'


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

    def toDict(self):
        return {
            'id': self.id
            # 'found': self.found,
            # 'place': self.place,
            # 'details': self.details
        }


class TfIdf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}

    def add_document(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        for w in list_of_words:
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0

        # normalizing the dictionary
        length = float(len(list_of_words))
        for k in doc_dict:
            doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict])

    def similarities(self, list_of_words):
        """Returns a list of all the [docname, similarity_score] pairs relative to a
list of words.

        """

        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            doc_dict = doc[1]
            for k in query_dict:
                if k in doc_dict:
                    score += (query_dict[k] / self.corpus_dict[k]) + (
                        doc_dict[k] / self.corpus_dict[k])
            sims.append([doc[0], score])

        return sims


# @app.route('/')
# def hello_world():
#     return '<h1>Hello World</h1>'


# @app.route('/post/<id>', methods=['GET'])
# def one_post(id):
#     posts = Post.query.filter_by(id=id).first()

#     data = json.dumps(posts.toDict())

#     response = Response(data, status=200, mimetype='application/json')
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response


# @app.route('/posts', methods=['GET'])
# def all_posts():
#     response_data = []

#     posts = Post.query.all()
#     for post in posts:
#         # print(post.toDict())
#         response_data.append(post.toDict())

#     data = json.dumps(response_data)

#     response = Response(data, status=200, mimetype='application/json')
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response


@app.route('/tfidf/<lost>/<place>', methods=['GET'])
def gettfidf(lost, place):
    response_data = []
    table = TfIdf()
    temp_lost = '%'+lost+'%'
    temp_place = '%'+place+'%'
    print(temp_lost)
    posts = Post.query.filter(Post.found.like(temp_lost)).filter(
        Post.place.like(temp_place)).all()
    for post in posts:
        table.add_document(str(post.id), post.details.split())
        # response_data.append(post.toDict())
    similar = table.similarities([lost, place])
    similar.sort(key=lambda x: x[1], reverse=True)
    for term in similar:
        response_data.append({'id': term[0], 'value': term[1]})
    data = json.dumps(response_data)
    response = Response(data, status=200, mimetype='application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# @app.route('/greetings/<lost>/<place>/<date>', methods=['GET'])
# def greetings(lost, area, date):
#     lost = request.args.get('lost')
#     area = request.args.get('area')
#     date = request.args.get('date')


#     return '''<h1>The language value is: {}</h1>
#               <h1>The framework value is: {}</h1>
#               <h1>The website value is: {}'''.format(lost, area, date)
