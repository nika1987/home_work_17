# app.py
import os
from flask import Flask, request
from flask_restx import Api, Resource
from db_setup.db_creat import db
from marshmallow import Schema, fields
from api.movie import movie_ns


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, instance_path=BASE_DIR)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api = Api(app)
api.add_namespace(movie_ns)





if __name__ == '__main__':
    app.run(debug=True)
