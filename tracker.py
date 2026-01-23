from flask import Flask, request , jsonify
import sqlite3
from datetime import date

tracker = Flask(__name__)
DB_NAME= "leetcode_tracker.db"


def get_db_connection():
    db_conn= sqlite3.connect(DB_NAME)
    db_conn.row_factory = sqlite3.Row
    return db_conn


def create_table():
    db_conn= get_db_connection()
    cursor= db_conn.execute("""
         CREATE TABLE IF NOT EXISTS leetcode_problems_tracker(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_solved TEXT,
            problem_number INTEGER,
            problem_name TEXT,
            difficulty TEXT,
            Notes TEXT
     )
""")
    
    db_conn.commit()
    db_conn.close()

    @tracker.route("/")
    def home():
        return jsonify({"Message": "Leetcode tracker API is running"})

    @tracker.route("/add", methods=["POST"])
    def add_problem():
        data= request.get_json()

        problem_name=data.get("problem_name")
        problem_number=data.get("problem_number")
        difficulty = data.get("difficulty")
        #topic= data.get("topic")
        Notes=data.get("Notes")
        

        if not problem_name:
           return jsonify({"error": "Problem name required"}), 400
        

        db_conn=get_db_connection()
        cursor= db_conn.cursor()
        cursor.execute("""
             INSERT INTO leetcode_problems_tracker
                       (date_solved, problem_name, problem_number, difficulty, Notes)
                       VALUES (?,?,?,?,?)""", 
        (
            date.today().isoformat(), 
            problem_name,
            problem_number,
            difficulty,
            Notes))
        
        
        db_conn.commit()
        db_conn.close()

        return jsonify({"Message":"Problem added succesfully"})
    

    @tracker.route("/problems", methods=["GET"])
    def get_problems():
        problem_number=request.args.get("problem_number")
        problem_name=request.args.get("problem_name")

        db_conn= get_db_connection()
        cursor= db_conn.cursor()

        if problem_number:
            cursor.execute(
                "SELECT * FROM leetcode_problems_tracker WHERE problem_number=?",
                (problem_number,)
            )
            rows=cursor.fetchall()

        elif problem_name:
            cursor.execute(
                "SELECT * FROM leetcode_problems_tracker WHERE problem_name LIKE ?",
                (f"%{problem_name}")
            )
            rows=cursor.fetchall()

        else:
            cursor.execute("SELECT * FROM leetcode_problems_tracker")
            rows = cursor.fetchall()



        db_conn.close()

        problems=[dict(row) for row in rows]
        return jsonify(problems), 200


if __name__ == "__main__":
    create_table()
    tracker.run(debug=True)    



        

