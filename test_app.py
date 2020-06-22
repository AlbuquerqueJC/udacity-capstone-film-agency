import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, Related, db_drop_and_create_all
from sqlalchemy import desc

db = SQLAlchemy()

bearer_tokens = dict(
    casting_assistant='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZzBNVU5ETlVFd1EwUkNRa00yTlVReVJqTkVSVU5HUVVKR1FUUTVNVE14UXpFelJUSkJSZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1wcm9qY2EuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTAxYzY0NGNlY2Q3MDAxM2Q1MDAwNSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkyODYyNDY2LCJleHAiOjE1OTI5NDg4NjYsImF6cCI6InBLclJxZFV0dm0xdVZ6MDZ4N3hKUW03Rk5HM0VDNzMyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.iishHKBmG_XeG2N1korBs7jKOd8sMK1CPTfR0UgtpBlmpSh1b4RXz2YJAjYRlGOvgU6VUAjj1z--gznN0oZifQZz4EtHTf8o-HJLmx6z4cI4oDI2XUZJxlNRndLC4jvw9AU2iaFTBZn6_En9LN1g_CZwGydMCl7M3h_NcdRbwp6D6AvCd5PQYH4PAsNHb9O7zHhI19x4Fit3lcwjtU5FdQLnEDDyZR4z8FdZQzn98LZcGY5lDniIrZs3kdmv4zh1h72RX79pZkyuWnPfy5oMzEwLyfUOHLszdwI3fAkfaQNeCSsMlLkUqJ2Bpb134_gisUk0h05zmlvJMTnLdITlqA',
    casting_director='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZzBNVU5ETlVFd1EwUkNRa00yTlVReVJqTkVSVU5HUVVKR1FUUTVNVE14UXpFelJUSkJSZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1wcm9qY2EuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZjEyNzMxMmRhOWJiMDAxMzZjNTQzYiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkyODYyNjUyLCJleHAiOjE1OTI5NDkwNTIsImF6cCI6InBLclJxZFV0dm0xdVZ6MDZ4N3hKUW03Rk5HM0VDNzMyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.iCFWKzZexaZWRD0Bz21Jo6jSo3nR4iAQaYWJmgSSgBoymqUuwDrwUx0oNZ4AQe3nnNKKzyg0a6f0uHmqO-8xapT5TAaqwNzd8AWUrbFYjG0aUsOLJS8xhqAwP5jbr1G9T6CMFfu6-IzuMowgfoy9IiRqvQZxlFALCrewLv7cvYqa0JQIRMZxIcjeCg2YizAi8cFC3deQDYqHi7eVMW_janVgC1_h79Q8avd9y71Pixp3dymOKYBehlb3tFSvPYi0-G-qCyPMqYsZLvxe5jCcNvqLMsY9X1DGvEhk3jGRb85cQN_2J-4IykKom9pPQGWsXDG3CHSLuJX4TR7J0-Va5Q',
    executive_producer='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZzBNVU5ETlVFd1EwUkNRa00yTlVReVJqTkVSVU5HUVVKR1FUUTVNVE14UXpFelJUSkJSZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1wcm9qY2EuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTAxMmVjYzBmNTFlMDAxOTVjYWU1OCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkyODYyNDA1LCJleHAiOjE1OTI5NDg4MDUsImF6cCI6InBLclJxZFV0dm0xdVZ6MDZ4N3hKUW03Rk5HM0VDNzMyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.VQ36G9JKz4Wc88ChgkNO0b4IsJN83fCJAD3jz2h6BEeIMPpY8wyOHQaGPn-ivX0NmjjuPqzkfOOEKSu2mxfEKXrrnqwnByiGvbxixz7NK4MpLqe0dwX3XHcXUGD0V4TiYoG9jWx4C70fqyxBNea9DbvIT2sqsBvMenSIdUYNPdCVvv4ir3nacKZ385P2DGmWkWvYZ8oR1kbymMtqQ9tQ7ybQVSjE1mJpvgiDe6BevG0FEb0831gpmrsQfPbTyn73Kt0rObg-tvf__NDw9qlYI0a9jCWIgIRCGJIFAUjrpD1iqvI0yrgfrAsjwMe6yFZvIIuufxrTW2kTdd0NyFTkAw'
    )

# Create dict with Authorization key and Bearer token as values.
# Later used by test classes as Header

casting_assistant_auth_header = {
    'Authorization': bearer_tokens['casting_assistant']
}

casting_director_auth_header = {
    'Authorization': bearer_tokens['casting_director']
}

executive_producer_auth_header = {
    'Authorization': bearer_tokens['executive_producer']
}

database_path = os.environ.get('DATABASE_URL', "postgresql://{}@{}:{}/{}".format(
    "postgres", "localhost", "5432", "capstone_test"))


def setup_db(app, database_path):
    """binds a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# ----------------------------------------------------------------------------#
# Tests I: Missing Authorization | Missing Authentication
#   Casting Assistant:
#   - test_error_401_get_all_movies (Authorization)
#   Casting Director:
#   - test_error_401_delete_actor (Authorization)
#   - test_error_403_delete_actor (Authentication)
#   Executive Producer:
#   - test_error_401_delete_movie (Authorization)
#   - test_error_403_delete_movie (Authentication)

# Tests II: Missing Authentication (i.e. missing permissions)
# ----------------------------------------------------------------------------#

# ----------------------------------------------------------------------------#
# Setup of Unittest
# ----------------------------------------------------------------------------#

class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test driven development (TDD): Create test cases first, then add
    # endpoints to pass tests

    # -------------------------------------------------------------------------#
    # Tests for /actors POST
    # -------------------------------------------------------------------------#

    def test_create_new_actor(self):
        """Test POST new actor."""

        json_create_actor = {
            'name'  : 'Joao',
            'age'   : 25,
            'gender': 'M'
        }

        res = self.client().post('/actors', json=json_create_actor,
                                 headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    def test_error_401_new_actor(self):
        """Test POST new actor w/o Authorization."""

        json_create_actor = {
            'name': 'Joao',
            'age' : 25
        }

        res = self.client().post('/actors', json=json_create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_422_create_new_actor(self):
        """Test Error POST new actor."""

        json_create_actor_without_name = {
            'age': 25
        }

        res = self.client().post('/actors', json=json_create_actor_without_name,
                                 headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'no name provided.')

    # -------------------------------------------------------------------------#
    # Tests for /actors GET
    # -------------------------------------------------------------------------#

    def test_get_all_actors(self):
        """Test GET all actors."""
        res = self.client().get('/actors?page=1',
                                headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_get_all_actors(self):
        """Test GET all actors w/o Authorization."""
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_404_get_actors(self):
        """Test Error GET all actors."""
        res = self.client().get('/actors?page=123',
                                headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # -------------------------------------------------------------------------#
    # Tests for /actors PATCH
    # -------------------------------------------------------------------------#

    def test_edit_actor(self):
        """Test PATCH existing actors"""
        json_edit_actor_with_new_age = {
            'age': 30
        }
        res = self.client().patch('/actors/1',
                                  json=json_edit_actor_with_new_age,
                                  headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)

    def test_error_400_edit_actor(self):
        """Test PATCH with non json body"""

        res = self.client().patch('/actors/123',
                                  headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], 'request does not contain a valid JSON body.')

    def test_error_404_edit_actor(self):
        """Test PATCH with non valid id"""
        json_edit_actor_with_new_age = {
            'age': 30
        }
        res = self.client().patch('/actors/123412',
                                  json=json_edit_actor_with_new_age,
                                  headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], 'Actor with id 123412 not found in database.')

    # -------------------------------------------------------------------------#
    # Tests for /actors DELETE
    # -------------------------------------------------------------------------#

    def test_error_401_delete_actor(self):
        """Test DELETE existing actor w/o Authorization"""
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_actor(self):
        """Test DELETE existing actor with missing permissions"""
        res = self.client().delete('/actors/1',
                                   headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_actor(self):
        """Test DELETE existing actor"""
        res = self.client().delete('/actors/1',
                                   headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_actor(self):
        """Test DELETE non existing actor"""
        res = self.client().delete('/actors/123',
                                   headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], 'Actor with id 123 not found in database.')

    # -------------------------------------------------------------------------#
    # Tests for /movies POST
    # -------------------------------------------------------------------------#

    def test_create_new_movie(self):
        """Test POST new movie."""

        json_create_movie = {
            'title'       : 'Joao Movie',
            'release_year': '1998'
        }

        res = self.client().post('/movies', json=json_create_movie,
                                 headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    def test_error_422_create_new_movie(self):
        """Test Error POST new movie."""

        json_create_movie_without_name = {
            'release_year': '1998'
        }

        res = self.client().post('/movies', json=json_create_movie_without_name,
                                 headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'no title provided.')

    # -------------------------------------------------------------------------#
    # Tests for /movies GET
    # -------------------------------------------------------------------------#

    def test_get_all_movies(self):
        """Test GET all movies."""
        res = self.client().get('/movies?page=1',
                                headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_error_401_get_all_movies(self):
        """Test GET all movies w/o Authorization."""
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_404_get_movies(self):
        """Test Error GET all movies."""
        res = self.client().get('/movies?page=123',
                                headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'no movies found in database.')

    # -------------------------------------------------------------------------#
    # Tests for /movies PATCH
    # -------------------------------------------------------------------------#

    def test_edit_movie(self):
        """Test PATCH existing movies"""
        json_edit_movie = {
            'release_year': '1998'
        }
        res = self.client().patch('/movies/1', json=json_edit_movie,
                                  headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)

    def test_error_400_edit_movie(self):
        """Test PATCH with non valid id json body"""
        res = self.client().patch('/movies/1',
                                  headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], 'request does not contain a valid JSON body.')

    def test_error_404_edit_movie(self):
        """Test PATCH with non valid id"""
        json_edit_movie = {
            'release_year': '1998'
        }
        res = self.client().patch('/movies/123412', json=json_edit_movie,
                                  headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], 'Movie with id 123412 not found in database.')

    # -------------------------------------------------------------------------#
    # Tests for /movies DELETE
    # -------------------------------------------------------------------------#

    def test_error_401_delete_movie(self):
        """Test DELETE existing movie w/o Authorization"""
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_movie(self):
        """Test DELETE existing movie with wrong permissions"""
        res = self.client().delete('/movies/1',
                                   headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie(self):
        """Test DELETE existing movie"""
        res = self.client().delete('/movies/1',
                                   headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_movie(self):
        """Test DELETE non existing movie"""
        res = self.client().delete('/movies/123',
                                   headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], 'Movie with id 123 not found in database.')


# Make the tests conveniently executable.
# From app directory, run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()
