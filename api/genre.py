from flask_restx import Resource, Namespace
from db_setup.models import Genre, GenreSchema


genre_ns = Namespace('genre')
genre_schema = GenreSchema()


@genre_ns.route('/')
class GenreList(Resource):
    def get(self):
        genre = Genre.query.all()
        return genre_schema.dump(genre, many=True)