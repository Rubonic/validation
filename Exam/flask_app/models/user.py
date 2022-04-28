from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, redirect
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# -------------------------------------------------------
class User:
    db = "exam_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.tvshows = []

# REGISTRATION
    @staticmethod
    def validate_register(form_data):
        is_valid = True
        if len(form_data["first_name"]) < 3:
            flash("First name must be at least 3 characters long!")
            is_valid = False
        if len(form_data["last_name"]) < 3:
            flash("Last name must be at least 3 characters long!")
            is_valid = False
        if len(form_data["email"]) < 3:
            flash("Email must be at least 3 characters long!")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Enter a Valid Email!")
            is_valid = False
        if len(form_data["password"]) < 8:
            flash("Password must be at least 8 characters long!")
            is_valid = False
        if form_data["password"] != form_data["confirm_password"]:
            flash("Both Passwords must match!")
            is_valid = False
        return is_valid

    @classmethod
    def register_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password, created_at) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW());"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

# LOGIN
    @staticmethod
    def validate_login(form_data):
        is_valid = True
        user_in_db = User.get_by_email(form_data)
        if not user_in_db:
            flash("Invalid Email/Password")
            is_valid = False
        elif not bcrypt.check_password_hash(user_in_db.password, form_data['password']):
            flash("Invalid Email/Password")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

# DASHBOARD
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
# --------------------------------------------------------------------------------