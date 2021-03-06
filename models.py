import os

import babel
import dateutil.parser
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()


def db_init_records():
    """Initialize the database with some records."""
    new_actor = (Actor(
        name='Joao Albuquerque',
        gender='M',
        age=38
    ))

    new_actor_girl = (Actor(
        name='April Albuquerque',
        gender='F',
        age=24
    ))

    new_actor_boy = (Actor(
        name='Jonathan Albuquerque',
        gender='M',
        age=26
    ))

    new_movie = (Movie(
        title='Joao is Amazing',
        release_year='1981'
    ))

    new_movie_girl = (Movie(
        title='Awesome April',
        release_year='2012'
    ))

    new_movie_boy = (Movie(
        title='The life of Jonathan',
        release_year='2010'
    ))

    new_movie_boy_and_girl = (Movie(
        title='Brother and Sister Code',
        release_year='2020'
    ))

    # Main and my movie
    new_actor.insert()
    new_movie.insert()
    Related(movie_id=new_movie.id, actor_id=new_actor.id).insert()
    # Girl and her movie
    new_actor_girl.insert()
    new_movie_girl.insert()
    Related(
        movie_id=new_movie_girl.id,
        actor_id=new_actor_girl.id
    ).insert()
    # Boy and his movie
    new_actor_boy.insert()
    new_movie_boy.insert()
    Related(
        movie_id=new_movie_boy.id,
        actor_id=new_actor_boy.id
    ).insert()
    # Girl and Boy Movie
    new_movie_boy_and_girl.insert()
    Related(
        movie_id=new_movie_boy_and_girl.id,
        actor_id=new_actor_boy.id
    ).insert()
    Related(
        movie_id=new_movie_boy_and_girl.id,
        actor_id=new_actor_girl.id
    ).insert()
    db.session.commit()


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


def actor_features_in(actor_id):
    # displays list of relationships between Actors and Movies
    relationship = Related.query.filter_by(actor_id=actor_id).all()
    data = []
    for relation in relationship:
        movie = Movie.query.filter_by(id=relation.movie_id).first()
        relation = {
            "id"            : relation.movie_id,
            "title"         : movie.title,
            "release_year"  : movie.release_year
        }
        data.append(relation)
    return data


def movie_actors(movie_id):
    # displays list of relationships between Actors and Movies
    relationship = Related.query.filter_by(movie_id=movie_id).all()
    data = []
    for relation in relationship:
        actor = Actor.query.filter_by(id=relation.actor_id).first()
        relation = {
            "id"    : relation.actor_id,
            "name"  : actor.name,
            "gender": actor.gender,
            "age"   : actor.age
        }
        data.append(relation)
    return data


'''
Actors
Have name, age, gender and what movies they star in'
Parent
'''


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    age = Column(Integer(), nullable=False)
    gender = Column(String(1), nullable=False)
    # Add movie as foreign key for actor model
    # movie_list = db.relationship("movie_list", secondary=movie_actor_table,
    # back_populates="actors")
    # movie_list = db.Column(db.Integer, db.ForeignKey('movie_list.id'), nullable=True)
    related = db.relationship('Related', backref='actor', uselist=False,
                              passive_deletes=True)

    # movie_list = db.relationship("Movie")

    def __init__(self, name, age, gender):
        self.name = name
        self.gender = gender
        self.age = age

    def format(self):
        return {
            'id'    : self.id,
            'name'  : self.name,
            'age'   : self.age,
            'gender': self.gender,
            'movies': actor_features_in(self.id)
        }

    '''
    short()
        short form representation of the Actor model
    '''

    def short(self):
        return {
            'id'    : self.id,
            'name'  : self.name,
            'age'   : self.age,
            'gender': self.gender
        }

    def long(self):
        return {
            'id'    : self.id,
            'name'  : self.name,
            'age'   : self.age,
            'gender': self.gender,
            'movies': actor_features_in(self.id)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            actor = Actor(title=req_title, release_year=req_date, 
            actor_id=req_actor_id)
            actor.insert()
    '''

    def insert(self):
        print(self)
        try:
            db.session.add(self)
            db.session.commit()
        except():
            print("Unable to add movie")
            db.session.rollback()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor(name=req_name)
            actor.delete()
    '''

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except():
            print("Unable to delete actor")
            db.session.rollback()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'Steven Seagull'
            actor.update()
    '''

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print({e})
            db.session.rollback()
        finally:
            db.session.commit()

    def __repr__(self):
        return json.dumps(self.long())


'''
Movies 
Have title and release date
Child
'''


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False, unique=True)
    release_year = Column(db.String(4), nullable=False)
    # Define parent-child relationship between the Movie and Actors
    # actors = db.relationship('Actor', secondary=Related, backref=db.backref(
    #    'Related', lazy='joined'))
    related = db.relationship('Related', backref='movie', lazy=True,
                              passive_deletes=True)

    # actor_list = db.relationship("actors", secondary=movie_actor_table,
    # back_populates="movie_list")

    def __init__(self, title, release_year):
        self.title = title
        self.release_year = release_year

    def format(self):
        return {
            'id'          : self.id,
            'title'       : self.title,
            'release_year': self.release_year,
            'actors'      : movie_actors(self.id)
        }

    '''
    short()
        short form representation of the Movie model
    '''

    def short(self):
        return {
            'id'          : self.id,
            'title'       : self.title,
            'release_year': self.release_year
        }

    def long(self):
        return {
            'id'          : self.id,
            'title'       : self.title,
            'release_year': self.release_year,
            'actors'      : movie_actors(self.id)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, release_year=req_date, 
            actor_id=req_actor_id)
            movie.insert()
    '''

    def insert(self):
        print(self)
        try:
            db.session.add(self)
            db.session.commit()
        except():
            print("Unable to add movie")
            db.session.rollback()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, release_year=req_date)
            movie.delete()
    '''

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except():
            print("Unable to delete movie")
            db.session.rollback()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Black Hawk'
            movie.update()
    '''

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print({e})
            db.session.rollback()
        finally:
            db.session.commit()

    def __repr__(self):
        return json.dumps(self.long())


class Related(db.Model):
    __tablename__ = 'Related'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id,
                                                   ondelete='CASCADE')
                         , nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey(Actor.id,
                                                   ondelete='CASCADE')
                         , nullable=False)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def format(self):
        return {
            'id'      : self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
        }

    def insert(self):
        print(self)
        try:
            db.session.add(self)
            db.session.commit()
        except():
            print("Unable to add relationship")
            db.session.rollback()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except():
            print("Unable to delete relationship")
            db.session.rollback()


'''
movie_actor_table = db.Table('movie_actor_table',
                             db.Model.metadata,
                             Column('movie_id', Integer,
                                    db.ForeignKey('Movie.id')),
                             Column('actor_id', Integer,
                                    db.ForeignKey('Actor.id')))
'''
