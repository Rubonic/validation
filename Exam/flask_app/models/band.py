from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, redirect
from flask_app import app
from flask_app.models import user
# -----------------------------------------------------------------------
class Band:
    db = "exam_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.band_name = data["band_name"]
        self.founding_member = data["founding_member"]
        self.genre = data["genre"]
        self.home_city = data["home_city"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        self.singers = {}
        
    @staticmethod
    def validate_band(form_data):
        is_valid = True
        if len(form_data["band_name"]) < 2:
            flash("Band name must be at least 2 characters long!")
            is_valid = False
        if len(form_data["genre"]) < 2:
            flash("Music Genre must be at least 2 characters long!")
            is_valid = False
        return is_valid

    @classmethod
    def create_band(cls, data):
        query = """
        INSERT INTO bands (band_name, genre, home_city, user_id, created_at) 
        VALUES (%(band_name)s, %(genre)s, %(home_city)s, %(user_id)s, NOW());"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results 

    @classmethod
    def get_all_bands(cls):
        query = "SELECT * FROM bands LEFT JOIN users ON bands.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_bands_with_singers = []
        for row in results:
            band = Band(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            band.singer = user.User(user_data)
            all_bands_with_singers.append(band)
        return all_bands_with_singers

    @classmethod
    def get_one_band(cls, data):
        query = "SELECT * FROM bands LEFT JOIN users ON bands.user_id = users.id WHERE bands.id = %(band_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        band = cls(results[0])

        user_data = {
            "id" : results[0]["users.id"],
            "first_name" : results[0]["first_name"],
            "last_name" : results[0]["last_name"],
            "email" : results[0]["email"],
            "password" : results[0]["password"],
            "created_at" : results[0]["users.created_at"],
            "updated_at" : results[0]["users.updated_at"]
        }
        band.remote = user.User(user_data)
        return band
# ----------------------------------------------------------------------------------------------------
# # Edit a network
#     @classmethod
#     def update_tvshow(cls, data):
#         query = "UPDATE tvshows SET name = %(name)s, network = %(network)s, time = %(time)s, description = %(description)s, updated_at = NOW() WHERE id = %(tvshow_id)s;"
#         results = connectToMySQL(cls.db).query_db(query, data)
#         return
# # -----------------------------------------------------------------------------------------------------
# # DELETE (NEEDS A WHERE STATEMENT)
#     @classmethod
#     def delete_tvshow(cls, data):
#         query = "DELETE FROM tvshows WHERE id = %(tvshow_id)s;"
#         results = connectToMySQL(cls.db).query_db(query, data)
#         return