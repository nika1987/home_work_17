from flask_restx import Resource, Namespace
from db_setup.models import Movie, MovieSchema


movie_ns = Namespace('movie')
movie_schema = MovieSchema()


@movie_ns.route('/')
class MovieList(Resource):
    def get(self):
        movies = Movie.query.all()
        return movie_schema.dump(movies, many=True)


@movie_ns.route('/<int:movie_id>')
class MovieDetail(Resource):
    def get(self, movie_id):
        movie = Movie.query.get(movie_id)
        return movie_schema.dump(movie)

