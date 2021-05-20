from flask import Flask, render_template, request, redirect, url_for
from chat_with_prof import get_user, create_table, get_db, checkpassword, get_account_type, list_of_prof,list_of_stu, new, set_default
from datetime import datetime
import sqlite3
from flask_socketio import SocketIO

app = Flask(__name__)


@app.route('/')
def index():
    set_default()
    return render_template('home.html')


@app.route('/survey_start/')
def survey_start():
    return render_template('1_start page.html')


@app.route('/survey_page/')
def survey_page():
    return render_template('2_survey.html')


@app.route('/personality/')
def personality():
    img = "../static/practical_car.png"
    personality = "Practical"
    desc = "You enjoy working with machines, mechanisms and tools, and you might be interested in physical or biological processes, as well as building and modelling! Let’s take a look at the possible jobs you may be interested in that are in this category!"
    return render_template('3_personality.html',
                           personality=personality,
                           desc=desc,
                           img=img)


@app.route('/jobs/')
def jobs():
    return render_template('4_job_options.html')


@app.route('/doctor/')
def doctor():
    pic = "../static/doctor.png"
    return render_template('5_job_desc.html', pic=pic)


@app.route('/courses/')
def courses():
    return render_template('6_course.html')

@app.route('/chat_with_prof_menu/')
def chat_with_prof_menu():
    if get_account_type() == "stu":
        prof_names = list_of_prof()
        print(prof_names)
        print(get_user())
        return render_template("chatwithprof_menu.html", names = prof_names)
    elif get_account_type() == "prof":
        stu_names = list_of_stu()
        return render_template("chatwithprof_menu.html", names = stu_names)

@app.route('/chat_with_profs/', methods = ["POST", "GET"])
def chat_with_profs():
    user = get_user()
    if user != "DLI":
        if request.method == "GET":
            if get_account_type() == "stu":
                prof = request.args["name"]
                try:
                    create_table("Chat" + str(user), "Prof" + prof)
                    return render_template('chatwithprof_sec.html', data = "data", user = str(user))
                except:
                    db_name = "Prof" + prof + ".db"
                    db = get_db(db_name)
                    print(prof)
                    print("A")
                    print("Chat" + str(user))
                    query = "SELECT * FROM {}".format("Chat" + str(user))
                    cursor = db.execute(query)
                    data = cursor.fetchall()
                    db.close()
                    print(data)
                    return render_template('chatwithprof_sec.html', data = data, user = str(user), db_name = db_name, choice = prof, stu = "")
            elif get_account_type() == "prof":
                stu = request.args["name"]
                try:
                    create_table("Chat" + stu, "Prof" + user)
                    return render_template('chatwithprof_sec.html', data = "data", user = user)
                except:
                    db_name = "Prof" + user + ".db"
                    db = get_db(db_name)
                    query = "SELECT * FROM {}".format("Chat" + stu)
                    cursor = db.execute(query)
                    data = cursor.fetchall()
                    db.close()
                    return render_template('chatwithprof_sec.html', data = data, user = user, db_name = db_name, choice = stu, stu = stu)
        else:
            name = request.form["Name"]
            message = request.form["Message"]
            db = request.form["db"]
            choice = request.form["choice"]
            stu = request.form["stu"]
            new(name, message, db, stu)
            return redirect(url_for("chat_with_profs", name = choice)) 
            
    else:
        return render_template('chatwithprof_sec.html', user = user)


@app.route('/login/', methods = ["POST", "GET"])
def login():
    message = ""
    result = ""
    if request.method == "GET":
        return render_template("login.html", checked = "1")
    else:
        username = request.form["username"]
        password = request.form["password"]
        message = checkpassword(username, password)
        if message == "S":
            result = "pass"
            
            
        elif message == "PC":
            result = "Password is not correct please retry"
        elif message == "UNF":
            result = "username not found"
        else:
            result = message
        return render_template("login.html", checked ="0", message = result)

@app.route("/signup/")
def signup():
    return "pass"


if __name__ == "__main__":
    app.run(debug=True)
