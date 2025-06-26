from flask import Blueprint, url_for, render_template
from app.db import get_db

home = Blueprint('home', __name__, template_folder='templates')

@home.route("/")
def index():
    return render_template("index.html")




@home.route("/test")
def test():
    return render_template("test.html")


@home.route("/message", methods=["GET"]) 
def message():
    
    db = get_db()
    cur = db.cursor()
       
    print("\n\n\n")
    print(cur.execute("SELECT * FROM image").fetchall())
    print("\n\n\n")

    return "Success!"
