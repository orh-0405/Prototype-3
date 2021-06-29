from flask import Flask, render_template, request, redirect, url_for
from chat_with_prof import get_user, create_table, get_db, checkpassword, get_account_type, list_of_prof,list_of_stu, new, set_default, account_exist, new_user
import os.path
from survey import open_survey
import sqlite3

curr_dir = os.path.dirname(__file__)

app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about_page.html')

@app.route('/survey_start/')
def survey_start():
    return render_template('1_start page.html')


@app.route('/survey_page/')
def survey_page():
    return render_template('2_survey.html')


@app.route('/test/', methods=["GET", "POST"])
def test():
    if request.method == "GET":
        questions = open_survey()
        for i in range(len(questions)):
            print(questions[i][1])
        return render_template('testtt.html', questions=questions)
    else:
        values = []
        for i in range(1,11):
            value = request.form[str(i)]
            values.append(value)
        return str(values)


@app.route('/personality/')
def personality():
    img = "../static/data_car.png"
    personality = "Data"
    desc = "You enjoy working with data such as numbers and percentages etc. You have good logic and would be good at jobs such as business finance and accounting!"

    #img = "../static/practical_car.png"
    #personality = "Practical"
    #desc = "You enjoy working with machines, mechanisms and tools, and you might be interested in physical or biological processes, as well as building and modelling! Let’s take a look at the possible jobs you may be interested in that are in this category!"
    return render_template('3_personality.html',
                           personality=personality,
                           desc=desc,
                           img=img)

@app.route('/get_jobs/<string:personality>/')
def get_jobs(personality):
    New_db_name = 'uni_database_file/' + personality + '_car' + '.db'
    print(New_db_name)
    db = sqlite3.connect(New_db_name)
    cursor = db.execute("SELECT * FROM Jobs_Avail")
    rows = cursor.fetchall()
    data = []
    for row in rows:
        jobs = row[2].split("\n")
        data.append([row[1], jobs, personality+"_car"])
    return render_template('4_job_options.html', data=data, New_db_name=New_db_name)


@app.route('/job_info/<string:job_chosen>/<string:db_name>/', methods = ['POST', 'GET'])
def job_info(job_chosen, db_name):
    print("HERE job info")
    New_db_name = 'uni_database_file/' + db_name + '.db'
    print(New_db_name)
    db = sqlite3.connect(New_db_name)
    print("JOb: ", job_chosen)
    
    if job_chosen in ["Doctor", "Veterinarian", "Pharmacist", "Physical therapists"]:
        job_chosen = "Medicine"

    if job_chosen in ["Business Sector", "Accountant"]:
        job_chosen = "Business_Accounting"

    if "Compute" in job_chosen:
        job_chosen = "Computing"
    
    print(job_chosen)
    cursor = db.execute(f"SELECT * FROM {job_chosen}")
    rows = cursor.fetchall()
    db.close()
    if request.method == "POST":
        print("POST METHOD")
        data = []
        for row in rows:
            #final = ""
            criteria = row[2]
            criteria = criteria.split('-')
            print("criteria.split()", criteria)
            #criteria[2] = criteria[0] + " " + criteria[1] + " " + criteria[2]
            print("??:",row[0], criteria[2])
            refs = row[4]
            refs = refs.split("\n")
            data.append([row[0],[row[1]],criteria,[row[3]], refs])
        print(data)
        return render_template('6_course.html', data=data, job_chosen=job_chosen)
    else:
        print("method: ", request.method)
        print('GET METHOD')
        print(db_name)
        descriptions = []
        for row in rows:
            descriptions.append(row[-2])
        return render_template('5_job_desc.html', 
                                descriptions=descriptions, 
                                job_chosen=job_chosen,
                                db_name=db_name)

@app.route('/chat_with_prof_menu/')
def chat_with_prof_menu():
    user = get_user()
    if user != "DLI":
        if get_account_type() == "stu":
            prof_names = list_of_prof()
            return render_template("chatwithprof_menu.html", names = prof_names)
        elif get_account_type() == "prof":
            stu_names = list_of_stu()
            return render_template("chatwithprof_menu.html", names = stu_names)
    else:
        return render_template('chatwithprof_sec.html', user = user)

@app.route('/chat_with_profs/', methods = ["POST", "GET"])
def chat_with_profs():
    user = get_user()
    if user != "DLI":
        if request.method == "GET":
            if get_account_type() == "stu":
                prof = request.args["name"]
                try:
                    create_table("Chat" + str(user), "Prof" + prof)
                    print("i")
                    return render_template('chatwithprof_sec.html', data = "data", user = str(user))
                except:
                    db_name = "Prof" + prof + ".db"
                    db = get_db(db_name)
                    query = "SELECT * FROM {}".format("Chat" + str(user))
                    cursor = db.execute(query)
                    data = cursor.fetchall()
                    db.close()
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

@app.route("/signup/", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("sign_up.html", checked = "0")
    else:
        name = request.form["username"]
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]
        acc = request.form["acc"]
        if password == confirmpassword:
            if account_exist(name) == False:
                new_user(name, password, acc)
                return render_template("sign_up.html", checked = "1", message = "pass")
            else:
                print("I")
                return render_template("sign_up.html", checked = "1", message = "User exist try another name")
        else:
            return render_template("sign_up.html", checked = "1", message = "Password does not match")



if __name__ == "__main__":
    run_once = 0
    if run_once == 0:
        set_default()
        run_once = 1
    app.run(debug=True)
