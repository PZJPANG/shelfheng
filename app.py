import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required
from database import db

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            errorcode = 400
            message = "must provide username"
            return render_template("apology.html", errorcode = errorcode, message = message)

        # Ensure password was submitted
        elif not request.form.get("password"):
            errorcode = 400
            message = "must provide password"
            return render_template("apology.html", errorcode = errorcode, message = message)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            errorcode = 400
            message = "invalid username/ password"
            return render_template("apology.html", errorcode = errorcode, message = message)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return render_template("mainpage.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Checking the validity of user
        session.clear()
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not username:
            errorcode = 400
            message = "Must provide username"
            return render_template("apology.html", errorcode = errorcode, message = message)
        elif not password:
            errorcode = 400
            message = "must provide password"
            return render_template("apology.html", errorcode = errorcode, message = message)
        elif not confirmation:
            errorcode = 400
            message = "must confirm your password"
            return render_template("apology.html", errorcode = errorcode, message = message)
        elif confirmation != password:
            errorcode = 400
            message = "confirmation not match"
            return render_template("apology.html", errorcode = errorcode, message = message)
        elif len(rows) != 0:
            errorcode = 400
            message = "username exist, try to login"
            return render_template("apology.html", errorcode = errorcode, message = message)
        else:
            # add new user into the database
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(password))

        # login the new user
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("register.html")


@app.route("/item", methods=["GET", "POST"])
@login_required
def item():
    # Join items with places to get house names
    items = db.execute("""
        SELECT i.*, p.name as house_name, p.address as house_address 
        FROM items i 
        LEFT JOIN places p ON i.place = CAST(p.id AS TEXT) 
        WHERE i.user_id = ? 
        ORDER BY i.item_id
    """, session["user_id"])
    return render_template("item.html", items = items)
    

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        if not request.form.get("name"):
            errorcode = 401
            message = "Must provide item name"
            return render_template("apology.html", errorcode = errorcode, message=message)
        db.execute("INSERT INTO items (name, place, shelf, user_id) VALUES (?, ?, ?, ?)", request.form.get("name"), request.form.get("place"), request.form.get("shelf"), session["user_id"])
        flash(f'Succesfully added "{request.form.get("name")}"')
        return redirect("/item")
    
    # Get available places (houses) for the current user
    places = db.execute("SELECT id, name FROM places WHERE user_id = ? ORDER BY name", session["user_id"])
    # Get all shelves for the current user (for initial load)
    shelves = db.execute("SELECT id, name, place_id FROM shelves WHERE user_id = ? ORDER BY name", session["user_id"])
    return render_template("add.html", places=places, shelves=shelves)


@app.route("/get_shelves/<int:house_id>")
@login_required
def get_shelves(house_id):
    # Get shelves for a specific house
    shelves = db.execute("SELECT id, name FROM shelves WHERE place_id = ? AND user_id = ? ORDER BY name", house_id, session["user_id"])
    return jsonify(shelves)

@app.route("/check", methods=["POST"])
@login_required
def check():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return {"exists": False}
    rows = db.execute("""
        SELECT p.name as house_name, i.shelf 
        FROM items i 
        LEFT JOIN places p ON i.place = CAST(p.id AS TEXT) 
        WHERE i.name = ? AND i.user_id = ?
    """, name, session["user_id"])
    if rows:
        return {"exists": True, "place": rows[0]["house_name"] or "Unknown", "shelf": rows[0]["shelf"]}
    return {"exists": False}

@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        item_ids = request.form.getlist("item_id")
        if item_ids:
            for item_id in item_ids:
                db.execute("DELETE FROM items WHERE item_id = ?", item_id)
        return redirect("/item")
    return redirect("/item")

@app.route("/search", methods=["GET", "POST"])
def search():
    items = []
    if request.method == "POST":
        q = request.form.get("q", "")
        if q:
            items = db.execute("""
                SELECT i.name, p.name as house_name, i.shelf 
                FROM items i 
                LEFT JOIN places p ON i.place = CAST(p.id AS TEXT) 
                WHERE i.name LIKE ? AND i.user_id = ?
            """, "%" + q + "%", session["user_id"])
    return render_template("search.html", items=items)

@app.route("/house", methods=["GET", "POST"])
@login_required
def house():
    # Get all houses/places for the current user
    houses = db.execute("SELECT * FROM places WHERE user_id = ?", session["user_id"])
    return render_template("house.html", houses=houses)

@app.route("/house/<int:house_id>/shelves")
@login_required
def house_shelves(house_id):
    # Get house details
    house = db.execute("SELECT * FROM places WHERE id = ? AND user_id = ?", house_id, session["user_id"])
    if not house:
        return render_template("apology.html", errorcode=404, message="House not found")
    
    # Get all shelves for this house
    shelves = db.execute("SELECT * FROM shelves WHERE place_id = ? AND user_id = ?", house_id, session["user_id"])
    return render_template("house_shelves.html", house=house[0], shelves=shelves)

@app.route("/shelf/<int:shelf_id>/items")
@login_required
def shelf_items(shelf_id):
    # Get shelf details
    shelf = db.execute("SELECT * FROM shelves WHERE id = ? AND user_id = ?", shelf_id, session["user_id"])
    if not shelf:
        return render_template("apology.html", errorcode=404, message="Shelf not found")
    
    # Get house details
    house = db.execute("SELECT * FROM places WHERE id = ? AND user_id = ?", shelf[0]["place_id"], session["user_id"])
    if not house:
        return render_template("apology.html", errorcode=404, message="House not found")
    
    # Get items in this shelf - both items and shelves now use "Shelf X" format
    items = db.execute("SELECT * FROM items WHERE place = ? AND shelf = ? AND user_id = ?", 
                      str(shelf[0]["place_id"]), shelf[0]["name"], session["user_id"])
    
    return render_template("shelf_items.html", shelf=shelf[0], house=house[0], items=items)

@app.route("/add_house", methods=["GET", "POST"])
@login_required
def add_house():
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        
        if not name:
            return render_template("apology.html", errorcode=400, message="Must provide house name")
        elif not address:
            return render_template("apology.html", errorcode=400, message="Must provide house address")
        
        # Add new house to database
        db.execute("INSERT INTO places (name, address, user_id) VALUES (?, ?, ?)", 
                  name, address, session["user_id"])
        
        flash(f'Successfully added "{name}"')
        return redirect("/house")
    
    return render_template("add_house.html")

@app.route("/house/<int:house_id>/add_shelf", methods=["GET", "POST"])
@login_required
def add_shelf(house_id):
    # Get house details
    house = db.execute("SELECT * FROM places WHERE id = ? AND user_id = ?", house_id, session["user_id"])
    if not house:
        return render_template("apology.html", errorcode=404, message="House not found")
    
    if request.method == "POST":
        name = request.form.get("name")
        
        if not name:
            return render_template("apology.html", errorcode=400, message="Must provide shelf name")
        
        # Add new shelf to database
        db.execute("INSERT INTO shelves (name, place_id, user_id) VALUES (?, ?, ?)", 
                  name, house_id, session["user_id"])
        
        flash(f'Successfully added "{name}"')
        return redirect(f"/house/{house_id}/shelves")
    
    return render_template("add_shelf.html", house=house[0])

@app.route("/delete_house/<int:house_id>", methods=["POST"])
@login_required
def delete_house(house_id):
    # Verify house belongs to user
    house = db.execute("SELECT * FROM places WHERE id = ? AND user_id = ?", house_id, session["user_id"])
    if not house:
        return render_template("apology.html", errorcode=404, message="House not found")
    
    # Delete all items in this house first
    db.execute("DELETE FROM items WHERE place = ? AND user_id = ?", str(house_id), session["user_id"])
    
    # Delete all shelves in this house
    db.execute("DELETE FROM shelves WHERE place_id = ? AND user_id = ?", house_id, session["user_id"])
    
    # Delete the house
    db.execute("DELETE FROM places WHERE id = ? AND user_id = ?", house_id, session["user_id"])
    
    flash(f'Successfully deleted "{house[0]["name"]}" and all its contents')
    return redirect("/house")

@app.route("/delete_shelf/<int:shelf_id>", methods=["POST"])
@login_required
def delete_shelf(shelf_id):
    # Get shelf details
    shelf = db.execute("SELECT * FROM shelves WHERE id = ? AND user_id = ?", shelf_id, session["user_id"])
    if not shelf:
        return render_template("apology.html", errorcode=404, message="Shelf not found")
    
    # Get house details for redirect
    house = db.execute("SELECT * FROM places WHERE id = ? AND user_id = ?", shelf[0]["place_id"], session["user_id"])
    
    # Delete all items in this shelf first
    db.execute("DELETE FROM items WHERE place = ? AND shelf = ? AND user_id = ?", 
              str(shelf[0]["place_id"]), shelf[0]["name"], session["user_id"])
    
    # Delete the shelf
    db.execute("DELETE FROM shelves WHERE id = ? AND user_id = ?", shelf_id, session["user_id"])
    
    flash(f'Successfully deleted "{shelf[0]["name"]}" and all its items')
    return redirect(f"/house/{shelf[0]['place_id']}/shelves")

@app.route("/mainpage")
@login_required
def mainpage():
    return render_template("mainpage.html")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))