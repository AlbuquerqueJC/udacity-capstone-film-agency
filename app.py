import json
import os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, Related, format_datetime, db
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    #
    # Helpers.
    #
    def relationships():
        # displays list of relationships between Actors and Movies
        relationship = Related.query.all()
        data = []
        for relation in relationship:
            relation = {
                "movie_id"        : relation.movie_id,
                "movie_name"      : Movie.query.get(relation.movie_id).title,
                "actor_id"        : relation.actor_id,
                "actor_name"      : Actor.query.get(relation.actor_id).name,
                "actor_gender"    : Actor.query.get(relation.actor_id).gender
            }
            data.append(relation)
        return data

    def actor_appears_in(actor_id):
        # displays list of relationships between Actors and Movies
        relationship = Related.query.filter_by(actor_id=actor_id).all()
        data = []
        for relation in relationship:
            relation = {
                "movie_id"        : relation.movie_id,
                "movie_name"      : Movie.query.get(relation.movie_id).title,
                "actor_id"        : relation.actor_id,
                "actor_name"      : Actor.query.get(relation.actor_id).name,
                "actor_gender"    : Actor.query.get(relation.actor_id).gender
            }
            data.append(relation)
        return data

    def actor_choices():
        # Adding the ID to the name in selectField
        choices = db.session.query(Actor.id, Actor.name).order_by(
            Actor.name).all()
        actor_choices = {}
        actors = []
        for choice in choices:
            id = choice[0]
            name = choice[1]
            new_name = 'ID: ' + str(id) + ' - ' + name
            actor_choices[id] = new_name
        actors = list(actor_choices.items())
        return actors

    def movie_choices():
        # Adding the ID to the name in selectField
        movie_choices = db.session.query(Movie.id, Movie.title).order_by(
            Movie.title).all()
        new_movie_choices = {}
        movies = []
        for movie_choice in movie_choices:
            id = movie_choice[0]
            title = movie_choice[1]
            new_title = 'ID: ' + str(id) + ' - ' + title
            new_movie_choices[id] = new_title
        movies = list(new_movie_choices.items())
        return movies

    def movie_choice(chosen_movie_id):
        # Adding the ID to the name in selectField
        movie_choices = db.session.query(Movie.id, Movie.title).order_by(
            Movie.title).filter_by(id=chosen_movie_id).first()
        new_movie_choice = {}
        movie = ()
        print("Movie Choices: ", movie_choices)
        id = movie_choices[0]
        title = movie_choices[1]
        new_movie_choice[id] = title
        movie = list(new_movie_choice.items())
        print("Movie return: ", movie)
        return movie_choices

    # ----------------------------------------------------------------------------#
    # Filters.
    # ----------------------------------------------------------------------------#
    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = 'localhost:8100'
        header[
            'Access-Control-Allow-Headers'] = 'Authorization, Content-Type, true'
        header[
            'Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE,PATCH,OPTIONS'
        return response

    # ----------------------------------------------------------------------------#
    # Routes.
    # ----------------------------------------------------------------------------#
    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"

        # return render_template('pages/home.html')
        return greeting

    #  RelationShip Tests
    #  ----------------------------------------------------------------
    @app.route('/relations')
    def relations():
        # displays list of relationship between Actors and Movies
        relationship = Related.query.all()
        data = []
        for relation in relationship:
            relation = {
                "movie_id"        : relation.movie_id,
                "movie_name"      : Movie.query.get(relation.movie_id).title,
                "actor_id"        : relation.actor_id,
                "actor_name"      : Actor.query.get(relation.actor_id).name,
                "actor_gender"    : Actor.query.get(relation.actor_id).gender
            }
            data.append(relation)

        result = {
            'success'      : True,
            'relationship' : data
        }
        return jsonify(result)

    @app.route('/relationships', methods=['GET'])
    def relationships():
        # Adding the ID to the name in selectField
        choices = db.session.query(Actor.id, Actor.name).order_by(
            Actor.name).all()
        actor_choices = {}
        actors = []
        for choice in choices:
            id = choice[0]
            name = choice[1]
            new_name = 'ID: ' + str(id) + ' - ' + name
            actor_choices[id] = new_name
        actors = list(actor_choices.items())

        # Adding the ID to the name in selectField
        movie_choices = db.session.query(Movie.id, Movie.title).order_by(
            Movie.title).all()
        new_movie_choices = {}
        movies = []
        for movie_choice in movie_choices:
            id = movie_choice[0]
            title = movie_choice[1]
            new_title = 'ID: ' + str(id) + ' - ' + title
            new_movie_choices[id] = new_title
        movies = list(new_movie_choices.items())

        result = {
            'success'       : True,
            'movie_choices' : movies,
            'actor_choices' : actors
        }
        return jsonify(result)

    # Show all movies
    @app.route('/movies/', methods=['GET'])
    @requires_auth("get:movies")
    def show_movies(token):
        # List all of the movies
        movies = list(map(Movie.long, Movie.query.all()))
        result = {
            'success': True,
            'movies' : movies
        }
        return jsonify(result)

    # Show all actors
    @app.route('/actors/', methods=['GET'])
    @requires_auth("get:actors")
    def show_actors(token):
        # List all of the actors
        actors = list(map(Actor.long, Actor.query.all()))
        result = {
            'success': True,
            'actors' : actors
        }
        return jsonify(result)

    '''
        POST /actor
            it should create a new row in the actors table
            it should require the 'post:actor' permission
            it should contain the actor.short() data representation
        returns status code 200 and json {"success": True, "actors": actor} 
            where actor is an array containing only the newly created actor
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actor', methods=['POST'])
    @requires_auth('post:actor')
    def add_actor(token):
        if request.data:
            body = request.get_json()
            name = body.get('name', None)
            gender = body.get('gender', None)
            age = body.get('age', None)
            movies = body.get('movies', None)

            if movies is not None:
                movie_data = Movie.query.filter_by(id=movies).first()
                print("Movie Data:")
                print(movie_data.long())
                actor = Actor(name=name, gender=gender, age=age)
                Actor.insert(actor)

                new_actor = Actor.query.filter_by(id=actor.id).first()
                print("New Actor:")
                print(new_actor.long())

                # Add relationship to Related table
                relation = Related(movie_id=movie_data.id,
                                   actor_id=new_actor.id)
                Related.insert(relation)

                new_relation = Related.query.filter_by(id=relation.id).first()
                print("New Relation")
                print(new_relation.format())

                return jsonify({
                    'success': True,
                    'actors' : [new_actor.long()]
                })

            else:
                actor = Actor(name=name, gender=gender, age=age)
                Actor.insert(actor)

                new_actor = Actor.query.filter_by(id=actor.id).first()
                print("New Actor:")
                print(new_actor.long())

                return jsonify({
                    'success': True,
                    'actors' : [new_actor.long()]
                })

        else:
            abort(422)

    # Post Movie
    @app.route('/movie', methods=['POST'])
    @requires_auth('post:movie')
    def add_movie(token):
        if request.data:
            body = request.get_json()
            title = body.get('title', None)
            release_year = body.get('release_year', None)

            movie = Movie(title=title, release_year=release_year)
            Movie.insert(movie)

            new_movie = Movie.query.filter_by(id=movie.id).first()

            return jsonify({
                'success': True,
                'movies' : [new_movie.long()]
            })
        else:
            abort(422)

    '''
        DELETE /actor/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actor' permission
        returns status code 200 and json {"success": True, "delete": id} where 
            id is the id of the deleted record or appropriate status code 
            indicating reason for failure
    '''
    @app.route('/actor/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(token, actor_id):
        try:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if actor is None:
                abort(404)

            relationship = Related.query.filter_by(
                actor_id=actor_id).all()
            if relationship is None:
                print("No relationships to delete")
            else:
                relationship.delete()
                print("Deleted relationships")

            actor.delete()
            print("Deleted actor: " + actor_id)

            return jsonify({
                'success': True,
                'deleted': actor_id
            })
        except():
            abort(422)

    # Delete Movie
    @app.route('/movie/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(token, movie_id):
        try:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if movie is None:
                abort(404)

            relationship = Related.query.filter_by(
                movie_id=movie_id).all()
            if relationship is None:
                print("No relationships to delete")
            else:
                relationship.delete()
                print("Deleted relationships")

            movie.delete()
            print("Deleted movie: " + movie_id)

            return jsonify({
                'success': True,
                'deleted': movie_id
            })
        except():
            abort(422)


    '''
        PATCH /actor/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:actor' permission
            it should contain the actor.short() data representation
        returns status code 200 and json {"success": True, "actors": actor} 
            where actor is an array containing only the updated actor
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actor/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def patch_actor(token, actor_id):
        data = request.get_json()
        name = data.get('name', None)
        gender = data.get('gender', None)
        age = data.get('age', None)
        movies = data.get('movies', None)

        try:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if actor is None:
                abort(404)
            else:
                print("Update For Actor:")
                print(actor.short())

            if name is not None:
                actor.name = name

            if gender is not None:
                actor.gender = gender

            if age is not None:
                actor.age = age

            if movies is not None:
                try:
                    movie_data = Movie.query.filter_by(id=movies).first()
                    print("Movie Data:")
                    print(movie_data.short())

                    # Add relationship to Related table
                    relation = Related(movie_id=movie_data.id,
                                       actor_id=actor.id)
                    Related.insert(relation)

                    new_relation = Related.query.filter_by(id=relation.id).first()
                    print("New Relation")
                    print(new_relation.format())
                except():
                    abort(404)

            print(actor.short())
            Actor.update(actor)

            updated_actor = Actor.query.filter_by(id=actor_id).first()

            return jsonify({
                'success': True,
                'actors' : [updated_actor.long()]
            })
        except():
            abort(422)

    # PATCH MODIFY Movie
    @app.route('/movie/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def patch_movie(token, movie_id):
        data = request.get_json()
        title = data.get('title', None)
        release_year = data.get('release_year', None)
        actors = data.get('actors', None)

        try:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if movie is None:
                abort(404)

            if title is not None:
                movie.title = title

            if release_year is not None:
                movie.release_year = release_year

            if actors is not None:
                movie.actors = actors

            print(movie.format())
            Movie.update(movie)

            updated_movie = Movie.query.filter_by(id=movie_id).first()

            return jsonify({
                'success': True,
                'actors' : [updated_movie.short()]
            })
        except:
            abort(422)

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route('/test')
    def test():
        database_path = os.environ['DATABASE_URL']
        excited = os.environ['EXCITED']
        message = "Is this excited? " + excited + "\r\n Database URL: " + database_path
        return message

    # ----------------------------------------------------------------------------#
    # Error Handling
    # ----------------------------------------------------------------------------#
    '''
    unprocessable entity
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error"  : 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error"  : 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
            "success"    : False,
            "error"      : 401,
            "message"    : "Unauthorized",
            "description": "The server could not verify that you are authorized!"
        }), 401

    '''
    error handler for AuthError 
    '''

    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response

    # ----------------------------------------------------------------------------#
    # Return app
    # ----------------------------------------------------------------------------#
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
