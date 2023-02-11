from flask_restx import Resource, Namespace
from flask import Flask, request, jsonify
from db_setup.models import Director,  DirectorSchema


movie_ns = Namespace('director').path('movie')
director_schema = DirectorSchema()

movie_ns.route('/movies')
class DirectorList(Resource):
    def get(self):
        director_id = request.value.get('director_id')
        return director_id.get('movies')
