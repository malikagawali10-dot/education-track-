from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE_NAME = "students.json"


def load_students():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except:
        return []


def save_students(students):
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


def get_statistics(students):

    marks = []

    for student in students:
        try:
            marks.append(float(student.get("marks", 0)))
        except:
            marks.append(0)

    if not marks:
        return {
            "total": 0,
            "average": 0,
            "highest": 0,
            "lowest": 0
        }

    return {
        "total": len(students),
        "average": sum(marks) / len(marks),
        "highest": max(marks),
        "lowest": min(marks)
    }


@app.route("/")
def home():

    students = load_students()

    stats = get_statistics(students)

    if students:
        top_student = max(
            students,
            key=lambda student: float(
                student.get("marks", 0)
            )
        )

        top_score = float(
            top_student.get("marks", 0)
        )

    else:
        top_score = 0

    return render_template(
        "index.html",
        students=students,
        top_score=top_score,
        **stats
    )


@app.route("/students")
def students_page():

    students = load_students()

    return render_template(
        "students.html",
        students=students
    )


@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        students = load_students()

        student = {
            "roll": request.form.get("roll", ""),
            "name": request.form.get("name", ""),
            "age": request.form.get("age", ""),
            "course": request.form.get("course", ""),
            "marks": float(request.form.get("marks", 0))
        }

        students.append(student)

        save_students(students)

        return redirect("/students")

    return render_template("add_student.html")


@app.route("/delete/<roll>")
def delete_student(roll):

    students = load_students()

    students = [
        student
        for student in students
        if str(student.get("roll", "")) != str(roll)
    ]

    save_students(students)

    return redirect("/students")


@app.route("/analytics")
def analytics():

    students = load_students()

    stats = get_statistics(students)

    return render_template(
        "analytics.html",
        students=students,
        **stats
    )


@app.route("/topper")
def topper():

    students = load_students()

    if students:

        top_student = max(
            students,
            key=lambda student: float(
                student.get("marks", 0)
            )
        )

    else:

        top_student = None

    return render_template(
        "topper.html",
        student=top_student
    )


@app.route("/admin")
def admin():

    students = load_students()

    stats = get_statistics(students)

    return render_template(
        "admin.html",
        students=students,
        total=stats["total"],
        average=stats["average"],
        highest=stats["highest"],
        lowest=stats["lowest"]
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )