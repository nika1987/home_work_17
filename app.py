# app.py
import os
from flask import Flask, request
from flask_restx import Api, Resource, Namespace
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields


BAS_DIR = os.path.join(os.path.dirname(__file__))
app = Flask(__name__, instance_path=BAS_DIR)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    tablename = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    tablename = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    tablename = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


# Готовим схему для сериализации и десериализации через маршмалоу
class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()

# Экзепляры MovieSchema для сер-ции и дес-ции в единственном объекте и во множественных объектах.
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# Устанавливаем Flask-RESTX. Создаем объект API и CBV для обработки GET-запроса
api = Api(app)
movies_ns = Namespace('movies')
api.add_namespace(movies_ns)
directors_ns = Namespace('directors')
api.add_namespace(directors_ns)
genres_ns = Namespace('genres')
api.add_namespace(genres_ns)



# Роуты со значениями под наши сущности

@movies_ns.route('/')
class MovieView(Resource):
    """
    Возвращает список всех фильмов, разделенный по страницам.
    """

    def get(self):
        dir_id = request.values.get('director_id')
        gen_id = request.values.get('genre_id')
        if dir_id:
            try:
                movies_by_director = db.session.query(Movie).filter(Movie.director_id == dir_id).all()
                return movies_schema.dump(movies_by_director), 200
            except Exception as e:
                return str(e), 404
        if dir_id and gen_id:
            try:
                movies_by_director = db.session.query(Movie).filter(Movie.director_id == dir_id,
                                                                    Movie.genre_id == gen_id).all()
                return movies_schema.dumps(movies_by_director), 200
            except Exception as e:
                return str(e), 404
        if gen_id:
            try:
                movies_by_genre = db.session.query(Movie).filter(Movie.genre_id == gen_id).all()
                return movies_schema.dumps(movies_by_genre), 200
            except Exception as e:
                return str(e), 404
        try:
            movies = db.session.query(Movie).all()
            return movies_schema.dumps(movies), 200
        except Exception as e:
            return str(e), 404

    def post(self):
        data = request.json
        try:
            movie = Movie(**data)
            db.session.add(movie)
            db.session.commit()
            return movie_schema.dump(movie), 201
        except Exception as e:
            return str(e), 400




@movies_ns.route('/<int:uid>')
class MovieView(Resource):
    """
    Возвращает подробную информацию о фильме.
    """

    def get(self, uid: int):
        try:
            movies = db.session.query(Movie).get(uid)
            return movie_schema.dumps(movies), 200
        except Exception as e:
            return str(e), 404

    def delete(self, uid: int):
        try:
            movie = db.session.query(Movie).get(uid)
            db.session.delete(movie)
            db.session.commit()
            return 'Удалено успешно', 200
        except Exception as e:
            return str(e), 404


@directors_ns.route('/directors/')
class DirectorView(Resource):
    """
    возвращает всех режиссеров
    """
    def get(self):
        try:
            directors = db.session.query(Director).all()
            return DirectorSchema().dump(directors, many=True), 200
        except Exception as e:
            return str(e), 404


@directors_ns.route('/<int:uid>')
class DirectorView(Resource):
    """
    возвращает подробную информацию о режиссере
    """
    def get(self, uid: int):
        try:
            director = db.session.query(Director).get(uid)
            return DirectorSchema().dump(director), 200
        except Exception as e:
            return str(e), 404

@genres_ns.route('/genres/')
class GenreView(Resource):
    """
    возвращает все жанры
    """
    def get(self):
        try:
            genres = db.session.query(Genre).all()
            return GenreSchema().dump(genres, many=True), 200
        except Exception as e:
            return str(e), 404


@genres_ns.route('/<int:uid>')
class GenreView(Resource):
    """
    возвращает подробную информацию о жанре

    """
    def get(self, uid: int):
        try:
            genre = db.session.query(Genre).get(uid)
            return GenreSchema().dump(genre), 200
        except Exception as e:
            return str(e), 404




app.run(debug=True)
