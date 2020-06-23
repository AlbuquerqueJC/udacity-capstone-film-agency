import os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, Related, db, db_drop_and_create_all
from auth.auth import AuthError, requires_auth

ROWS_PER_PAGE = 5
data = []


# Create our app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Uncomment to re-initialize DB and create test records.
    # db_drop_and_create_all()

    #
    # Helpers.
    #
    def diff(first, second):
        """
        Calculated difference between two arrays
        Parameters:
          * An array [1,2,3,4]
          * Another array [2,5]
        Returns:
          * <array> difference of first array excluding the items from second
          array.
        """
        second = set(second)
        return [item for item in first if item not in second]

    def paginate_results(request, selection):
        """
        Paginates and formats database queries
        Parameters:
          * <HTTP object> request, that may contain a "page" value
          * <database selection> selection of objects, queried from database
        Returns:
          * <list> list of dictionaries of objects limit set by ROWS_PER_PAGE
        """
        # Get page from request. If not given, default to 1
        page = request.args.get('page', 1, type=int)

        # Calculate start and end slicing
        start = (page - 1) * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE

        # Format selection into list of dicts and return sliced
        objects_formatted = [object_name.format() for object_name in selection]
        return objects_formatted[start:end]

    # -------------------------------------------------------------------------#
    # Filters.
    # -------------------------------------------------------------------------#
    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        header[
            'Access-Control-Allow-Headers'] = 'Authorization, Content-Type, ' \
                                              'true '
        header[
            'Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE,PATCH,' \
                                              'OPTIONS '
        return response

    # -------------------------------------------------------------------------#
    # Routes.
    # -------------------------------------------------------------------------#
    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"

        # return render_template('pages/home.html')
        return greeting

    #  RelationShip Views
    #  ----------------------------------------------------------------
    @app.route('/relationships')
    def show_relationships():
        # displays list of relationship between Actors and Movies
        relationship = Related.query.all()
        print(relationship)
        paginated_relationship = paginate_results(request, relationship)

        if not paginated_relationship:
            abort(404, {'message': 'No relationships to list'})

        for relation in paginated_relationship:
            relation = {
                "id"          : relation['id'],
                "movie_id"    : relation['movie_id'],
                "movie_name"  : Movie.query.get(relation['movie_id']).title,
                "actor_id"    : relation['actor_id'],
                "actor_name"  : Actor.query.get(relation['actor_id']).name,
                "actor_gender": Actor.query.get(relation['actor_id']).gender
            }
            data.append(relation)

        result = {
            'success'      : True,
            'relationships': data
        }
        return jsonify(result)

    # Delete Relationship
    @app.route('/relationships/<relationship_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_relationship(token, relationship_id):
        try:
            if not relationship_id:
                abort(400, {
                    'message': 'please add relationship id to the request '
                               'url.'
                })

            relation = Related.query.filter_by(id=relationship_id).one_or_none()
            if not relation:
                abort(404, {
                    'message': 'Relationship with id {} not found in database.'
                               .format(relationship_id)
                })

            relation.delete()
            print("Deleted relationship: ", relationship_id)

            return jsonify({
                'success': True,
                'deleted': relationship_id
            })
        except():
            abort(422)

    @app.route('/relations', methods=['GET'])
    def relations():
        # Adding the ID to the name for Select Field
        actor_options = db.session.query(Actor.id, Actor.name).order_by(
            Actor.name).all()
        actor_choices = {}
        for choice in actor_options:
            id = choice[0]
            name = choice[1]
            new_name = 'ID: ' + str(id) + ' - ' + name
            actor_choices[id] = new_name
        actors = list(actor_choices.items())

        # Adding the ID to the name for Select Field
        movie_options = db.session.query(Movie.id, Movie.title).order_by(
            Movie.title).all()
        new_movie_choices = {}
        for movie in movie_options:
            id = movie[0]
            title = movie[1]
            new_title = 'ID: ' + str(id) + ' - ' + title
            new_movie_choices[id] = new_title
        movies = list(new_movie_choices.items())

        result = {
            'success'      : True,
            'movie_choices': movies,
            'actor_choices': actors
        }
        return jsonify(result)

    #  Movies Views
    #  ----------------------------------------------------------------
    @app.route('/movies', methods=['GET'])
    @requires_auth("get:movies")
    def show_movies(token):  # token
        # List all of the movies
        selection = Movie.query.all()
        paginated_movies = paginate_results(request, selection)

        if not paginated_movies:
            abort(404, {'message': 'No movies to list'})

        result = {
            'success': True,
            'movies' : paginated_movies
        }
        return jsonify(result)

    #  Actor Views
    #  ----------------------------------------------------------------
    @app.route('/actors', methods=['GET'])
    @requires_auth("get:actors")
    def show_actors(token):  # token
        # List all of the actors
        selection = Actor.query.all()
        paginated_actors = paginate_results(request, selection)

        if not paginated_actors:
            abort(404, {'message': 'No actors to list'})

        result = {
            'success': True,
            'actors' : paginated_actors
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

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def add_actor(token):
        if request.data:
            body = request.get_json()
            name = body.get('name', None)
            gender = body.get('gender', None)
            age = body.get('age', None)
            movies = body.get('movies', None)

            if not body:
                abort(400, {
                    'message': 'request does not contain a valid JSON '
                               'body.'
                })
            else:
                print("Data for Insert Actor:")
                print(body)

            if not name:
                abort(422, {'message': 'no name provided.'})

            if not age:
                abort(422, {'message': 'no age provided.'})

            if not gender:
                abort(422, {'message': 'no gender provided.'})

            actor = Actor(name=name, gender=gender, age=age)
            Actor.insert(actor)

            new_actor = Actor.query.filter_by(id=actor.id).first()
            print("New Actor:")
            print(new_actor.long())

            # Handling movie relationships
            if movies:
                # We add a relationship between actor and the movie(s)
                # Iterate through movie_ids in movies
                list_of_movies = []
                for movie in movies:
                    movie_data = Movie.query.filter_by(id=movie).one_or_none()
                    if not movie_data:
                        abort(422, {
                            'message': 'movie {} not found'.format(
                                movie)
                        })

                    # add this movie to list_of_movies
                    list_of_movies.append(movie_data.short())

                    # Add relationship to Related table
                    relation = Related(movie_id=movie_data.id,
                                       actor_id=new_actor.id)
                    relation.insert()

                    new_relation = Related.query.filter_by(
                        id=relation.id).first()
                    print("New Relation")
                    print(new_relation.format())

                print("List of movies", list_of_movies)

            return jsonify({
                'success': True,
                'actor'  : [new_actor.long()]
            })
        else:
            abort(422)

    # Post Movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def add_movie(token):
        if request.data:
            body = request.get_json()
            title = body.get('title', None)
            release_year = body.get('release_year', None)

            if not title:
                abort(422, {'message': 'no title provided.'})

            if not release_year:
                abort(422, {'message': 'no release_year provided.'})

            movie = Movie(title=title, release_year=release_year)
            Movie.insert(movie)

            new_movie = Movie.query.filter_by(id=movie.id).first()

            return jsonify({
                'success': True,
                'movie'  : [new_movie.long()]
            })
        else:
            abort(422)

    '''
        DELETE /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actor' permission
        returns status code 200 and json {"success": True, "delete": id} where 
            id is the id of the deleted record or appropriate status code 
            indicating reason for failure
    '''

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(token, actor_id):
        try:
            if not actor_id:
                abort(400, {
                    'message': 'please add actor id to the request url.'
                })

            actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if not actor:
                abort(404, {
                    'message': 'Actor with id {} not found in '
                               'database.'.format(actor_id)
                })

            relationship = Related.query.filter_by(
                actor_id=actor_id).all()

            if not relationship:
                print("No relationships to delete for actor_id:", actor_id)
            else:
                for relation in relationship:
                    relation.delete()
                    print("Deleted relationship movie {} for actor_id:".format(
                        relation.movie_id), actor_id)

            actor.delete()
            print("Deleted actor: ", actor_id)

            return jsonify({
                'success': True,
                'deleted': actor_id
            })
        except():
            abort(422)

    # Delete Movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(token, movie_id):
        try:
            if not movie_id:
                abort(400, {
                    'message': 'please add movie id to the request url.'
                })

            movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if not movie:
                abort(404, {
                    'message': 'Movie with id {} not found in '
                               'database.'
                      .format(movie_id)
                })

            relationship = Related.query.filter_by(movie_id=movie_id).all()

            if not relationship:
                print("No relationships to delete for movie_id:", movie_id)
            else:
                for relation in relationship:
                    relation.delete()
                    print("Deleted relationships for movie_id:", movie_id)

            movie.delete()
            print("Deleted movie: ", movie_id)

            return jsonify({
                'success': True,
                'deleted': movie_id
            })
        except():
            abort(422)

    '''
        PATCH /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:actor' permission
            it should contain the actor.short() data representation
        returns status code 200 and json {"success": True, "actors": actor} 
            where actor is an array containing only the updated actor
            or appropriate status code indicating reason for failure
    '''

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def patch_actor(token, actor_id):
        try:
            body = request.get_json()
            name = body.get('name', None)
            gender = body.get('gender', None)
            age = body.get('age', None)
            movies = body.get('movies', None)

            if not name and not age and not gender and not movies:
                abort(400, {
                    'message': 'at least one field needs to be changed.'
                })

            print("Data for Update Actor:")
            print(body)
        except():
            abort(400, {
                'message': 'request does not contain a valid JSON body.'
            })

        try:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if not actor:
                abort(404, {
                    'message': 'Actor with id {} not found in '
                               'database.'.format(actor_id)
                })
            else:
                print("Update For Actor:", actor_id)
                print(actor.short())

            if name is not None:
                actor.name = name

            if gender is not None:
                actor.gender = gender

            if age is not None:
                actor.age = age

            # Handling movie relationships
            list_of_movies = []
            list_of_movies_to_add = []
            already_exist_movies = []
            if movies:
                # We check existing relationship between actor and the movie(s)
                already_related_movies = Related.query.filter_by(
                    actor_id=actor_id).all()
                # Iterate through movie_ids in already_related_movies and
                # save to array
                for related_movie in already_related_movies:
                    already_exist_movies.append(related_movie.movie_id)

                print("Already Exists movies - Relationship already exists:",
                      already_exist_movies)
                # Check difference of movies to add vs already existing
                list_of_movies_to_add = diff(movies, already_exist_movies)
                print("Difference of already-exists-movies and movies is:",
                      list_of_movies_to_add)

                if not list_of_movies_to_add:
                    print("No movies to update")
                else:
                    for movie in list_of_movies_to_add:
                        movie_data = Movie.query.filter_by(
                            id=movie).one_or_none()
                        if not movie_data:
                            abort(422, {
                                'message': 'movie {} not found'.format(
                                    movie)
                            })

                        # add this movie to list_of_movies
                        list_of_movies.append(movie_data.short())

                        # Add relationship to Related table
                        relation = Related(movie_id=movie_data.id,
                                           actor_id=actor_id)
                        relation.insert()

                        print("New Relation")
                        print(relation.format())
                        print("List of movies", list_of_movies)

            if age or gender or name is not None:
                Actor.update(actor)
                updated_actor = Actor.query.filter_by(id=actor_id).first()
                print(updated_actor.long())
                return jsonify({
                    'success': True,
                    'actor'  : [updated_actor.long()]
                })
            elif not list_of_movies_to_add:
                abort(400, {
                    'message': 'at least one field needs to be changed.'
                })
            else:
                return jsonify({
                    'success': True,
                    'actor'  : [actor.long()]
                })
        except():
            abort(422)

    # PATCH MODIFY Movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def patch_movie(token, movie_id):
        try:
            body = request.get_json()
            title = body.get('title', None)
            release_year = body.get('release_year', None)
            actors = body.get('actors', None)

            print("Data for Update Movie:")
            print(body)
        except():
            abort(400, {
                'message': 'request does not contain a valid JSON body.'
            })

        if not title and not release_year:
            abort(400, {
                'message': 'at least one field needs to be changed.'
            })

        try:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if not movie:
                abort(404, {
                    'message': 'Movie with id {} not found in '
                               'database.'
                      .format(movie_id)
                })

            if title is not None:
                movie.title = title

            if release_year is not None:
                movie.release_year = release_year

            # TODO: Add ability to modify actors featuring in by movie_id
            # if actors is not None:
            #     movie.actors = actors

            print(movie.format())
            Movie.update(movie)

            updated_movie = Movie.query.filter_by(id=movie_id).first()

            return jsonify({
                'success': True,
                'movie'  : [updated_movie.short()]
            })
        except():
            abort(422)

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    # -------------------------------------------------------------------------#
    # Error Handling
    # -------------------------------------------------------------------------#
    def get_error_message(error, default_text):
        """
        Returns default error text or custom error message (if not applicable)
        *Input:
            * <error> system generated error message containing a description
            message
            * <string> default text to be used if Error has no specific message
        *Output:
            * <string> specific error message or default text (if no message)
        """
        try:
            # Return message contained in error
            return error.description['message']
        except():
            # else return default
            return default_text

    @app.errorhandler(422)
    def unprocessable(error, description="unprocessable"):
        return jsonify({
            "success": False,
            "error"  : 422,
            "message": get_error_message(error, "unprocessable!")
        }), 422

    @app.errorhandler(404)
    def not_found(error, description="resource not found"):
        return jsonify({
            "success": False,
            "error"  : 404,
            "message": get_error_message(error, "resource not found!")
        }), 404

    @app.errorhandler(400)
    def bad_request(error, description="bad request"):
        return jsonify({
            "success": False,
            "error"  : 400,
            "message": get_error_message(error, "bad request")
        }), 400

    @app.errorhandler(401)
    def unauthorized(error, description="Unauthorized!"):
        return jsonify({
            "success"    : False,
            "error"      : 401,
            "message"    : "Unauthorized",
            "description": get_error_message(error, "Unauthorized!")
        }), 401

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error"  : 500,
            "message": get_error_message(error, "Internal Server Error")
        }), 500

    @app.errorhandler(AuthError)
    def authentication_failed(AuthError):
        return jsonify({
            "success": False,
            "error"  : AuthError.status_code,
            "message": AuthError.error['description']
        }), AuthError.status_code

    # -------------------------------------------------------------------------#
    # Return app
    # -------------------------------------------------------------------------#
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
