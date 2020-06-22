# Capstone Film Agency

## Getting Setup

Public URL: 
https://jca-heroku-test.herokuapp.com

> _tip_: this API is designed to work with POSTMAN and Auth0

### Installing Dependencies

#### Installing Python Requirements

This project needs to install requirements
```bash
python install -r requirements.txt
```

## Required Tasks

### Configure Environment Variables

Environment variables. 

- Open `./setup.sh` and ensure each variable reflects the system you stood up
 for the backend.

## Running Your API

```bash
gunicorn -b :8080 app:app
```

### Authentication

The authentication system used for this project is Auth0. 
`./test_app.py` contains the bearer tokens necessary to test.

Accounts:
- executive@capstone.com | Password: "ExecutiveProducer!"
- director@capstone.com | Password: "Casting!"
- assistant@capstone.com | Password: "Assistant!"

casting_assistant_bearer_token=
```eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZzBNVU5ETlVFd1EwUkNRa00yTlVReVJqTkVSVU5HUVVKR1FUUTVNVE14UXpFelJUSkJSZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1wcm9qY2EuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTAxYzY0NGNlY2Q3MDAxM2Q1MDAwNSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkyODYyNDY2LCJleHAiOjE1OTI5NDg4NjYsImF6cCI6InBLclJxZFV0dm0xdVZ6MDZ4N3hKUW03Rk5HM0VDNzMyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.iishHKBmG_XeG2N1korBs7jKOd8sMK1CPTfR0UgtpBlmpSh1b4RXz2YJAjYRlGOvgU6VUAjj1z--gznN0oZifQZz4EtHTf8o-HJLmx6z4cI4oDI2XUZJxlNRndLC4jvw9AU2iaFTBZn6_En9LN1g_CZwGydMCl7M3h_NcdRbwp6D6AvCd5PQYH4PAsNHb9O7zHhI19x4Fit3lcwjtU5FdQLnEDDyZR4z8FdZQzn98LZcGY5lDniIrZs3kdmv4zh1h72RX79pZkyuWnPfy5oMzEwLyfUOHLszdwI3fAkfaQNeCSsMlLkUqJ2Bpb134_gisUk0h05zmlvJMTnLdITlqA```


casting_director_bearer_token=
```eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZzBNVU5ETlVFd1EwUkNRa00yTlVReVJqTkVSVU5HUVVKR1FUUTVNVE14UXpFelJUSkJSZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1wcm9qY2EuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZjEyNzMxMmRhOWJiMDAxMzZjNTQzYiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkyODYyNjUyLCJleHAiOjE1OTI5NDkwNTIsImF6cCI6InBLclJxZFV0dm0xdVZ6MDZ4N3hKUW03Rk5HM0VDNzMyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.iCFWKzZexaZWRD0Bz21Jo6jSo3nR4iAQaYWJmgSSgBoymqUuwDrwUx0oNZ4AQe3nnNKKzyg0a6f0uHmqO-8xapT5TAaqwNzd8AWUrbFYjG0aUsOLJS8xhqAwP5jbr1G9T6CMFfu6-IzuMowgfoy9IiRqvQZxlFALCrewLv7cvYqa0JQIRMZxIcjeCg2YizAi8cFC3deQDYqHi7eVMW_janVgC1_h79Q8avd9y71Pixp3dymOKYBehlb3tFSvPYi0-G-qCyPMqYsZLvxe5jCcNvqLMsY9X1DGvEhk3jGRb85cQN_2J-4IykKom9pPQGWsXDG3CHSLuJX4TR7J0-Va5Q```


executive_producer_bearer_token=
```eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJqZzBNVU5ETlVFd1EwUkNRa00yTlVReVJqTkVSVU5HUVVKR1FUUTVNVE14UXpFelJUSkJSZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1wcm9qY2EuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTAxMmVjYzBmNTFlMDAxOTVjYWU1OCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkyODYyNDA1LCJleHAiOjE1OTI5NDg4MDUsImF6cCI6InBLclJxZFV0dm0xdVZ6MDZ4N3hKUW03Rk5HM0VDNzMyIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.VQ36G9JKz4Wc88ChgkNO0b4IsJN83fCJAD3jz2h6BEeIMPpY8wyOHQaGPn-ivX0NmjjuPqzkfOOEKSu2mxfEKXrrnqwnByiGvbxixz7NK4MpLqe0dwX3XHcXUGD0V4TiYoG9jWx4C70fqyxBNea9DbvIT2sqsBvMenSIdUYNPdCVvv4ir3nacKZ385P2DGmWkWvYZ8oR1kbymMtqQ9tQ7ybQVSjE1mJpvgiDe6BevG0FEb0831gpmrsQfPbTyn73Kt0rObg-tvf__NDw9qlYI0a9jCWIgIRCGJIFAUjrpD1iqvI0yrgfrAsjwMe6yFZvIIuufxrTW2kTdd0NyFTkAw```
   

### Authorization

The Auth0 JWT includes claims for permissions based on the user's role within
 the Auth0 system.  This project makes use of these claims using the `auth
 .can(permission)` method which checks if particular permissions exist
  within the JWT permissions claim of the currently logged in user.
  
## EndPoints
#### GET /
health check and returns "Hello!!!!!!!!" if excited=True

#### GET /movies?page=<integer>
Returns JSON of paginated movies for page=<int>
```json
{
    "movies": [
        {
            "actors": [
                {
                    "age": 24,
                    "gender": "F",
                    "id": 2,
                    "name": "April Albuquerque"
                }
            ],
            "id": 2,
            "release_year": "2012",
            "title": "Awesome April"
        },
        {
            "actors": [
                {
                    "age": 26,
                    "gender": "M",
                    "id": 3,
                    "name": "Jonathan Albuquerque"
                },
                {
                    "age": 38,
                    "gender": "M",
                    "id": 4,
                    "name": "Amazing Me"
                }
            ],
            "id": 3,
            "release_year": "2010",
            "title": "The life of Jonathan"
        },
        {
            "actors": [
                {
                    "age": 26,
                    "gender": "M",
                    "id": 3,
                    "name": "Jonathan Albuquerque"
                },
                {
                    "age": 24,
                    "gender": "F",
                    "id": 2,
                    "name": "April Albuquerque"
                }
            ],
            "id": 4,
            "release_year": "2020",
            "title": "Brother and Sister Code"
        },
        {
            "actors": [
                {
                    "age": 38,
                    "gender": "M",
                    "id": 1,
                    "name": "Joao Albuquerque"
                },
                {
                    "age": 38,
                    "gender": "M",
                    "id": 4,
                    "name": "Amazing Me"
                }
            ],
            "id": 1,
            "release_year": "2008",
            "title": "Top Dogz"
        }
    ],
    "success": true
}
```
#### POST /movies
Adds movie from JSON values
`Request body:`
```json
{
    "title": "Joao Amazing",
    "release_year": "2020"
}
```

`Request response`
```json
{
    "movies": [
        {
            "actors": [],
            "id": 5,
            "release_year": "2020",
            "title": "Joao Amazing"
        }
    ],
    "success": true
}
```
#### PATCH /movies/<id>
Modifies movie <id> with JSON values
`Request body:`
```json
{
    "release_year": "2012"
}
```
`Request response`
```json
{
    "actors": [
        {
            "id": 5,
            "release_year": "2012",
            "title": "Joao Amazing"
        }
    ],
    "success": true
}
```
#### DELETE /movies/<id>
Deletes movie <id>
```json
{
    "deleted": 5,
    "success": true
}
```

#### GET /actors?page=<integer>
Returns JSON of paginated actors for page=<int>
```json
{
    "actors": [
        {
            "age": 38,
            "gender": "M",
            "id": 1,
            "movies": [
                {
                    "id": 1,
                    "release_year": "2008",
                    "title": "Top Dogz"
                }
            ],
            "name": "Joao Albuquerque"
        },
        {
            "age": 24,
            "gender": "F",
            "id": 2,
            "movies": [
                {
                    "id": 2,
                    "release_year": "2012",
                    "title": "Awesome April"
                },
                {
                    "id": 4,
                    "release_year": "2020",
                    "title": "Brother and Sister Code"
                }
            ],
            "name": "April Albuquerque"
        },
        {
            "age": 26,
            "gender": "M",
            "id": 3,
            "movies": [
                {
                    "id": 3,
                    "release_year": "2010",
                    "title": "The life of Jonathan"
                },
                {
                    "id": 4,
                    "release_year": "2020",
                    "title": "Brother and Sister Code"
                }
            ],
            "name": "Jonathan Albuquerque"
        },
        {
            "age": 38,
            "gender": "M",
            "id": 4,
            "movies": [
                {
                    "id": 3,
                    "release_year": "2010",
                    "title": "The life of Jonathan"
                },
                {
                    "id": 1,
                    "release_year": "2008",
                    "title": "Top Dogz"
                }
            ],
            "name": "Amazing Me"
        }
    ],
    "success": true
}
```
#### POST /actors
Adds actor from JSON values.
`Request body:`
```json
{
    "name": "Amazing Me",
    "gender": "M",
    "age": 38,
    "movies": [1,2]
}
```
`Request response:`
```json
{
    "actor": [
        {
            "age": 38,
            "gender": "M",
            "id": 6,
            "movies": [
                {
                    "id": 1,
                    "release_year": "2008",
                    "title": "Top Dogz"
                },
                {
                    "id": 2,
                    "release_year": "2012",
                    "title": "Top Cats"
                }
            ],
            "name": "Amazing J"
        }
    ],
    "success": true
}
```
#### PATCH /actors/<id>
Modifies actor <id> with JSON values
`Request body`
```json
{
    "age": 38,
    "movies": []
}
```
`Request response`
```json
{
    "actors": [
        {
            "age": 38,
            "gender": "M",
            "id": 4,
            "movies": [
                {
                    "id": 1,
                    "release_year": "2008",
                    "title": "Top Dogz"
                }
            ],
            "name": "Amazing Me"
        }
    ],
    "success": true
}
```
#### DELETE /actors/<id>
Deletes actor <id>
```json
{
    "deleted": 6,
    "success": true
}
```

#### GET /relationships?page=<integer>
Returns JSON of paginated relationships in database
```json
{
    "relationships": [
        {
            "actor_gender": "M",
            "actor_id": 4,
            "actor_name": "Amazing Me",
            "id": 13,
            "movie_id": 1,
            "movie_name": "Top Dogz"
        }
    ],
    "success": true
}
```

#### DELETE /relationships/<id>
Deletes relationship <id>
```json
{
    "deleted": "13",
    "success": true
}
```

#### GET /relations
Returns JSON options of available movies and actors to relate
```json
{
    "actor_choices": [
        [
            2,
            "ID: 2 - April Albuquerque"
        ],
        [
            1,
            "ID: 1 - Joao Albuquerque"
        ],
        [
            3,
            "ID: 3 - Jonathan Albuquerque"
        ]
    ],
    "movie_choices": [
        [
            2,
            "ID: 2 - Awesome April"
        ],
        [
            4,
            "ID: 4 - Brother and Sister Code"
        ],
        [
            1,
            "ID: 1 - Joao is Amazing"
        ],
        [
            3,
            "ID: 3 - The life of Jonathan"
        ]
    ],
    "success": true
}
```