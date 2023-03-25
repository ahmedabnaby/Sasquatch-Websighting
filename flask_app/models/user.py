from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import sighting
from flask import flash, session
import re 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

db = 'examhh_db'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def register(cls,data):
        if not cls.validate_user(data):
            return False
        form_data = cls.search_form(data)
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(db).query_db(query, form_data)
        session['user_id'] = user_id
        return user_id


    @classmethod
    def get_user_email(cls, email):
        data = {'email' : email}
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL(db).query_db(query, data)
        if results:
            results = cls(results[0])
        return results
    
    @classmethod
    def get_user_id(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(db).query_db(query, data)
        if results:
            results = cls(results[0])
        return results

    @classmethod
    def skeptic(cls, data):
        query = """
        INSERT INTO skeptics (sighting_id, user_id)
        VALUES (%(sighting_id)s, %(user_id)s)
        ;"""
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def believe(cls, data):
        query = """
        DELETE FROM skeptics
        WHERE sighting_id = %(sighting_id)s
        AND user_id = %(user_id)s
        ;"""
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def login(data):
        this_user = User.get_user_email(data['email'].lower())
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                return True
        flash("Login information is incorrect.", 'login')
        return False

    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters long.', 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters long.', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters long.', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", 'register')
            is_valid = False
        if User.get_user_email(data['email'].lower()):
            flash("Email is already registered.", 'register')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match", 'register')
            is_valid = False
        return is_valid
    

    @staticmethod
    def search_form(data):
        form_data = {}
        form_data['first_name'] = data['first_name']
        form_data['last_name'] = data['last_name']
        form_data['password'] = bcrypt.generate_password_hash(data['password'])
        form_data['email'] = data['email'].lower()
        return form_data

