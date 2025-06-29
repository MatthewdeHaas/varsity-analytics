from flask import Blueprint, url_for, render_template
from app.db import get_db
from app.analytics import *
import json

home = Blueprint('home', __name__, template_folder='templates')

@home.route("/")
def index():

    db = get_db()
    cur = db.cursor()

    schools = cur.execute("""
    SELECT name FROM school
    """).fetchall()

    return render_template("index.html", schools=schools)




@home.route("/school/<school>")
def school(school):
    
    db = get_db()
    cur = db.cursor()


    school = cur.execute("""
    SELECT * FROM school
    WHERE name = ?
    """, (school, )).fetchone()


    athletes = cur.execute("""
                   SELECT * FROM athlete
                   WHERE school_id = ?
    """, (school["id"], )).fetchall()

    sport_ids = tuple(set([athlete["sport_id"] for athlete in athletes]))
    sport_placeholders = str(["?" for _ in  range(len(sport_ids))]).replace("[", "(").replace("]", ")").replace("'", "")

    sports = cur.execute(f"""
                 SELECT * FROM sport
                 WHERE id in {sport_placeholders} 
    """, sport_ids).fetchall()

    athlete_ids = tuple([athlete["id"] for athlete in athletes])
    img_placeholders = str(["?" for _ in  range(len(athlete_ids))]).replace("[", "(").replace("]", ")").replace("'", "")

    images = cur.execute(f"""
             SELECT * FROM image
             WHERE athlete_id IN {img_placeholders}
    """, athlete_ids).fetchall()

    
    for athlete in athletes:

        sport_id_index = 0
        for i, sport in enumerate(sports):
            if sport["id"] == athlete["sport_id"]:
                sport_id_index = i
                break

        athlete["sport"] = sports[sport_id_index]
        athlete["images"] = [img for img in images if img["athlete_id"] == athlete["id"]]


    return render_template("school.html", school=school, athletes=athletes)



@home.route("/database/update")
def update_database():

    db = get_db()
    cur = db.cursor()

    schools = get_school_json_data(path="app/data/all_schools_data.json")

    # Insert schools and sports
    for name, school_data in schools.items():
        cur.execute("""
            INSERT OR IGNORE INTO school (name)
            VALUES(?)
        """, (name, ))

        for sport, athletes in school_data.items():
            cur.execute("""
                INSERT OR IGNORE INTO sport (name)
                VALUES(?)
            """, (sport, ))


    # Insert athletes
    for school_name, school_data in schools.items():

        school_id = cur.execute("""
                        SELECT name, id FROM school
                        WHERE name = ?
        """, (school_name, )).fetchone()["id"]
 

        for sport, athletes in school_data.items():

            sport_id = cur.execute("""
                           SELECT name, id FROM sport
                           WHERE name = ?
            """, (sport, )).fetchone()["id"]

            for athlete in athletes:

                misc = json.dumps({k:v for k, v in athlete.items() if k not in ["id", "name", "gender", "school_url", "sport", "images"]})

                if athlete["gender"] not in ["M", "F"]:
                    athlete["gender"] = "M"

                cur.execute("""
                    INSERT INTO athlete (athlete_key, name, gender, misc, sport_id, school_id)
                    VALUES(?, ?, ?, ?, ?, ?)
                """, (athlete["id"], athlete["name"], athlete["gender"].strip().replace("\"", ""), misc, sport_id, school_id))



    # Insert images
    for name, school_data in schools.items():
        for sport, athletes in school_data.items():
            for athlete in athletes:

                athlete_id = cur.execute("""
                                 SELECT id, name FROM athlete
                                 WHERE name = ?
                """, (athlete["name"], )).fetchone()["id"]

                for image in athlete["images"]:
                    cur.execute("""
                        INSERT INTO image (url, athlete_id)
                        VALUES(?, ?)
                    """, (image, athlete_id))

                    


    db.commit()
    
    return "Database updated!"


@home.route("/database/delete")
def delete_database():

    db = get_db()
    cur = db.cursor()

    for table in ["school", "sport", "athlete", "image"]:
        cur.execute(f"DELETE FROM {table}")

    db.commit()

    return "Database Deleted"



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
