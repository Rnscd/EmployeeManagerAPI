from flask import Flask, request, jsonify
import json
import sqlite3
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
Api = Api(app)
auth = HTTPBasicAuth()
USER_DATA = {
    "admin": "111"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("employees.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/employees", methods=["GET", "POST"])
@auth.login_required
def employees():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM employee")
        employees =  cursor.fetchall()
        
        if employees is not None:
            return jsonify(employees)

    if request.method == "POST":
        new_name = request.form["name"]
        new_email = request.form["email"]
        new_department = request.form["department"]
        new_salary = request.form["salary"]
        new_birth = request.form["birth"]
        sql = """INSERT INTO employee (name, email, department, salary, birth)
                 VALUES (?, ?, ?, ?, ?)"""
        cursor = cursor.execute(sql, (new_name, new_email, new_department, new_salary, new_birth))
        conn.commit()
        return f"Employee with id: {cursor.lastrowid} has been created."


@app.route("/employees/<int:id>", methods=["GET", "PUT", "DELETE"])
@auth.login_required
def single_employee(id):
    conn = db_connection()
    cursor = conn.cursor()
    employee = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM employee WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            employee = r
        if employee is not None:
            return jsonify(employee), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """UPDATE employee
                SET name=?,
                    email=?,
                    department=?
                WHERE id=? """

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        salary = request.form["salary"]
        birth = request.form["birth"]



        updated_employee = {
            "id": id,
            "name": name,
            "email": email,
            "department": department,
            "salary": salary,
            "birth": birth,
        }
        conn.execute(sql, (name, email, department, id))
        conn.commit()
        return jsonify(updated_employee)

    if request.method == "DELETE":
        sql = """ DELETE FROM employee WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The employee with id: {} has been deleted.".format(id), 200


@app.route("/reports/employees/salary", methods=["GET"])
@auth.login_required
def salary():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
     cursor = conn.execute("SELECT avg(salary) FROM employee")
     avgsalary = cursor.fetchall()
     cursor2 = conn.execute("SELECT * FROM employee WHERE salary = (select min(salary) FROM employee)")
     minsalary = cursor2.fetchall()
     cursor3 = conn.execute("SELECT * FROM employee WHERE salary = (select max(salary) FROM employee)")
     maxsalary = cursor3.fetchone()

     return jsonify("average:", avgsalary, "lowest:", minsalary, "highest:", maxsalary) 

  
               




@app.route("/reports/employees/age", methods=["GET"])
@auth.login_required
def age():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == "GET":
     cursor = conn.execute("SELECT * FROM employee WHERE birth = (select min(birth) FROM employee)")
     minsalary = cursor.fetchall()
     cursor2 = conn.execute("SELECT * FROM employee WHERE birth = (select max(birth) FROM employee)")
     maxsalary = cursor2.fetchone()
     cursor3 = conn.execute("SELECT avg(birth) FROM employee")
     avgsalary = cursor3.fetchall()
    
     return jsonify("average:", avgsalary, "oldest:", minsalary, "youngest:", maxsalary) 



     

if __name__ == "__main__":
    app.run(debug=True)
