from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash, session
import re 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

db = 'examhh_db'

class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_seen = data['date_seen']
        self.num_seen = data['num_seen']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.host = None
        self.skeptics = []

    @classmethod
    def add_sighting(cls,data):
        if not cls.validate_sighting(data):
            return False
        query = """
        INSERT INTO sightings (location, what_happened, date_seen, num_seen, user_id)
        VALUES (%(location)s, %(what_happened)s, %(date_seen)s, %(num_seen)s, %(user_id)s)
        ;"""
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def update_sighting(cls, data):
        if not cls.validate_sighting(data):
            return False
        query = """
        UPDATE sightings
        SET location = %(location)s, what_happened = %(what_happened)s,
        date_seen = %(date_seen)s, num_seen = %(num_seen)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(db).query_db(query, data)
        return True

    @classmethod
    def get_sighting_id(cls, data):
        query = """
        SELECT * FROM sightings
        JOIN users ON sightings.user_id = users.id
        LEFT JOIN skeptics ON sightings.id = skeptics.sighting_id
        LEFT JOIN users AS skeptic ON skeptics.user_id = skeptic.id
        WHERE sightings.id = %(id)s
        ;"""
        results = connectToMySQL(db).query_db(query, data)
        if results:
            row = results[0]
            sighting = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : '',
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            sighting.host = user.User(user_data)
            for row in results:
                if row['skeptic.id'] == None:
                    break
                skeptic_data = {
                    'id' : row['skeptic.id'],
                'first_name' : row['skeptic.first_name'],
                'last_name' : row['skeptic.last_name'],
                'email' : row['skeptic.email'],
                'password' : '',
                'created_at' : row['skeptic.created_at'],
                'updated_at' : row['skeptic.updated_at']
                }
                sighting.skeptics.append(user.User(skeptic_data))
            return sighting

    @classmethod
    def get_all_sightings(cls):
        query = """
        SELECT * FROM sightings
        JOIN users ON sightings.user_id = users.id
        LEFT JOIN skeptics ON sightings.id = skeptics.sighting_id
        LEFT JOIN users AS users2 on users2.id = skeptics.user_id
        ;"""
        results = connectToMySQL(db).query_db(query)
        print(results)
        sightings = []
        if results:
            for row in results:
                new_sighting = True
                skeptic_user_data = {
                    'id' : row['users2.id'],
                    'first_name' : row['users2.first_name'],
                    'last_name' : row['users2.last_name'],
                    'email' : row['users2.email'],
                    'password' : '',
                    'created_at' : row['users2.created_at'],
                    'updated_at' : row['users2.updated_at']
                }
                if len(sightings) > 0 and sightings[-1].id == row['id']:
                    sightings[-1].skeptics.append(user.User(skeptic_user_data))
                    new_sighting = False
                if new_sighting:
                    sighting = cls(row)
                    user_data = {
                        'id' : row['users.id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'email' : row['email'],
                    'password' : '',
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                    }
                    this_user = user.User(user_data)
                    sighting.host = this_user
                    if row['users2.id'] is not None:
                        sighting.skeptics.append(user.User(skeptic_user_data))
                    sightings.append(sighting)
        return sightings

    @classmethod
    def delete_sighting(cls, data):
        query = """
        DELETE FROM sightings
        WHERE id = %(id)s
        ;"""
        connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_sighting(data):
        is_valid = True
        if len(data['location']) < 1:
            flash("Location is required.")
            is_valid = False
        if len(data['what_happened']) < 1:
            flash("What Happened is required.")
            is_valid = False
        if len(data['date_seen']) < 1:
            flash("Date of Siting is required.")
            is_valid = False
        if len(data['num_seen']) < 1 :
            flash("# of Sasquatches must be at least 1.")
            is_valid = False
        return is_valid
