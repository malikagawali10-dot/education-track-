from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE_NAME = "students.json"


def load_students():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return []
    return []


def save_students(students):
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


@app.route("/")
def home():
    students = load_students()
    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():

    students = load_students()

    roll = request.form.get("roll", "").strip()

    # Check duplicate roll number
    for student in students:
        if str(student["roll"]) == roll:
            return "Roll Number already exists! <br><br><a href='/'>Go Back</a>"

    student = {
        "roll": roll,
        "name": request.form.get("name", "").strip(),
        "age": request.form.get("age", "").strip(),
        "course": request.form.get("course", "").strip(),
        "marks": float(request.form.get("marks", 0))
    }

    students.append(student)

    save_students(students)

    return redirect("/")


@app.route("/delete/<roll>")
def delete_student(roll):

    students = load_students()

    students = [
        student
        for student in students
        if str(student["roll"]) != str(roll)
    ]

    save_students(students)

    return redirect("/")


@app.route("/search")
def search():

    query = request.args.get(
        "query",
        ""
    ).lower().strip()

    students = load_students()

    if query:

        students = [
            student
            for student in students

            if query in str(student["roll"]).lower()
            or query in student["name"].lower()
            or query in student["course"].lower()
        ]

    return render_template(
        "index.html",
        students=students
    )


@app.route("/topper")
def topper():

    students = load_students()

    return render_template(
        "index.html",
        students=students
    )


@app.route("/statistics")
def statistics():

    students = load_students()

    return render_template(
        "index.html",
        students=students
    )


if __name__ == "__main__":
    app.run(debug=True)