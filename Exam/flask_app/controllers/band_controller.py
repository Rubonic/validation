from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.band import Band
# --------------------------------------------------------------------------
# New Route for TV Show
@app.route("/band/new")
def new_band():
    if 'user_id' not in session:
        flash("You need to login in order to continue!")
        return redirect("/")
    return render_template("new_band.html")

@app.route("/band/create", methods=["POST"])
def create_band():
    if not Band.validate_band(request.form):
        return redirect("/band/new")
    query_data = {
        "band_name" : request.form["band_name"],
        "found_member" : request.form["founding_member"],
        "genre" : request.form["genre"],
        "home_city" : request.form["home_city"],
        "user_id" : session["user_id"]
    }
    new_band_id = Band.create_band(query_data)
    return redirect("/dashboard")
# ----------------------------------------------------------------------------------
# Getting to view 1 network
@app.route("/band/show/<int:band_id>")
def show_band(band_id):
    if 'user_id' not in session:
        flash("You need to login in order to continue!")
        return redirect("/")
    query_data = {
        "band_id" : band_id
    }
    band = Band.get_one_band(query_data)
    return render_template("show_band.html", one_band = tband)
# -------------------------------------------------------------------------------------
# EDITING A NETWORK
@app.route("/band/edit/<int:band_id>")
def edit_band(band_id):
    if 'user_id' not in session:
        flash("You need to login in order to continue!")
        return redirect("/")
    query_data = {
        "band_id" : band_id
    }
    tvshow = Band.get_one_band(query_data)
    return render_template("edit_band.html", one_band = band)

@app.route("/band/update/<int:band_id>", methods=["POST"])
def update_band(band_id):
    if not Band.validate_band(request.form):
        return redirect(f"/band/edit/{band_id}")
    query_data = {
        "band_name" : request.form["band_name"],
        "found_member" : request.form["founding_member"],
        "genre" : request.form["genre"],
        "home_city" : request.form["home_city"],
        "band_id" : band_id
    }
    Band.update_band(query_data)
    return redirect("/dashboard")
# ------------------------------------------------------------------------------------------
# DELETE FUNCTION
@app.route("/band/delete/<int:band_id>")
def delete_band(band_id):
    query_data = {
        "band_id" : band_id
    }
    Band.delete_band(query_data)
    return redirect("/dashboard")
