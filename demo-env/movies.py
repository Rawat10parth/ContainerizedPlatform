from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from werkzeug.exception import abort
from models import Movies
from config import Config

movies_bp =Blueprint('movies', __name__)

# Fetches list of movies based on trendings which has (> 95%) users ratings
@movies_bp.route(Config.Trending_Now, methods=['GET'])
@jwt_required
def trending_now(username):
    if get_jwt_identity() == username:
        movies =Movies.objects()
        trending = []
        for movie in movies:
            # Checking if movie has more than 95% ratings
            if movie.ratings> 95:
                trending.append(movie)
        return make_response(jsonify(trending), 200)
    else:
       abort(401) 

# Fetches list of movies based on username
@movies_bp.route(Config.FETCH_MOVIES, methods=['GET'])
@jwt_required
def search_movie(username, title):
    if get_jwt_identity() == username:
        try:
            return make_response(jsonify(Movies.object.get(title=title)), 200)
        except Movies.DoesnotExist:
            abort(404)
        else:
            abort(401)

# User can add/remove movies as per their favourites
@movies_bp.route(Config.ADD_TO_FAVOURITE, methods=['PUT'])
@jwt_required
def add_to_favourite(username,title):
    if get_jwt_identity() == username:
        movie = Movies.objects(title=title).first()
        # Abort if no movie found
        if movie ==None:
            abort(404)

        movie.update(is_favourite=request.json['is_favourite'])

        if request.json['is_fovourite']:
            message = title+' has been added to your favourite'
        else:
            message = title+' has been removed from your favourite'

        return make_response(jsonify(
        {
            "success": message
        }
        ), 200)
    else:
        abort(401)

#Fetch list of favourite movies based
@movies_bp.route(Config.FAVOURITE_MOVIES, methods=['GET'])
@jwt_required
def favourite_movies(username):
    if get_jwt_identity() == username:
        return make_response(jsonify(Movies.objects(is_favourite=True)), 200)
    else:
        abort(401)
        
#Admin add movies into database
@movies_bp.route(Config.ADD_MOVIE, methods=['POST'])
@jwt_required
def add_movie(username):
    if username=='admin':
        if get_jwt_identity() == username:
            try:
                movies = Movies(title=request.json['title'],
                                movie_type=request.json['movie_type'],
                                ratings=request.json['ratings'],
                                duration=request.json['duration'],
                                age_restriction=request.json['age_restriction'],
                                timestamp=request.json['timestamp'],
                                thumbnails=request.json['thumbnails'],
                                media=request.json['media'],
                                subtitles=request.json['subtitles'],
                                description=request.json['description'],
                                cast=request.json['cast'],
                                genres=request.json['genres'],
                                category=request.json['category'],
                                production=request.json['production'],
                                country=request.json['country'],
                                is_favourite=request.json['is_favourite'])
                movies.save()
            except KeyError:
                abort(400)
            
            return make_response(jsonify({"success":'Movies Addedd Successfully'}), 201)
        else:
            abort(401)
    else:
        abort(401)

@movies_bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Sorry movie not found'}), 404)           

@movies_bp.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error' : 'Invalid Request '+error }))

@movies_bp.errorhandler(401)
def unathorized(error):
    return make_response(jsonify({'error' : 'Unathorized Access'}), 401)