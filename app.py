from flask import Flask, render_template, request, redirect, url_for
from chat_with_prof import get_db
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
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


@app.route('/chat_with_profs/')
def chat_with_profs():
    db = get_db()
    query = "SELECT * FROM Chat"
    cursor = db.execute(query)
    data = cursor.fetchall()
    db.close()
    return render_template('chatwithprof_sec.html', data = data)

@app.route("/new/", methods = ["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("chat with profs new.html")
    else:
        print(request.form)
        db = get_db()
        query = "INSERT INTO Chat (Name, Message, Time) VALUES(?,?,?)"
        now = datetime.now()  #gets current time
        current_time = now.strftime("%H:%M")
        db.execute(query, (request.form["Name"], request.form["Message"], current_time))

        db.commit()
        db.close()
        
        return redirect(url_for("chat_with_profs"))
@app.route('/login/')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
