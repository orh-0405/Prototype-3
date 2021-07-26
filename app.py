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
    questions = open_survey()
    for i in range(len(questions)):
        print(questions[i][1])
    return render_template('2_survey.html', questions=questions)


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


@app.route('/personality/', methods = ["POST"])
def personality():
    scores = {"Social":0 , "Practical":0 , "Data":0 , "Creative":0}
    answers = []
    print(request.form["1"])
    for i in range(1, 11):
        ans = request.form[str(i)]
        question_ans_pair = [i, ans]
        answers.append(question_ans_pair)
    print(answers)

    social_qns = [1, 10]
    prac_qns = [2,6]
    data_qns = [3,5,8]
    creative_qns = [4,7,9]
    qns_list = [["Social", social_qns],["Practical", prac_qns],\
        ["Data", data_qns],["Creative", creative_qns]]

    for cat in qns_list:
        category = cat[0]
        print(category)
        qns = cat[1]
        for qn in qns:
            for ans in answers:
                if ans[0] == qn:
                    print(qn, ans)
                    if qn <= 6 and ans[1] == "Yes":
                        scores[category] += 1
                    elif qn > 6:
                        scores[category] += int(ans[1])

    info = {"Social":["../static/social_car.jpeg", "You are a dedicated leader, humanistic, responsible and supportive. You use feelings, words and ideas to work with people rather than physical activity to do things. You enjoy closeness, sharing, groups, unstructured activity and being in charge. JObs that allow you to interact with people will be jobs that you will love!"] , \
        "Practical":["../static/practical_car.png", "You a good sense of prioritizing work. Maintaining a logical order of tasks is your biggest strength. Confidence and ability to make rational decisions in life is the significant quality of a practical person. You don't just assume things and act, but rather know what they are doing. You enjoy working with machines, mechanisms and tools, and you might be interested in physical or biological processes, as well as building and modelling! Let’s take a look at the possible jobs you may be interested in that are in this category!"] , \
            "Data":["../static/data_car.png", "You enjoy working with data such as numbers and percentages etc. You have good logic and would be good at jobs such as business finance and accounting!"], \
                "Creative":["../static/creative_car.jpeg", "You like to daydream and imagine the possibilities and wonders of the world. You can immerse yourself in imagination and fantasy, yet remain grounded enough to turn their daydreams into reality. You are often described as a dreamer, but that doesn't mean that you live with your heads in the clouds. Jobs in the creative industry are very fitted for you, including those of art, media and writing!"]}

    key_list = list(scores.keys())
    val_list = list(scores.values())
    position = val_list.index(max(val_list))
    personality = key_list[position]
    img = info[personality][0]
    desc = info[personality][1]

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

    if job_chosen in ['Therapist', 'Case Manager', 'Licensed Practical Nurse', 'Staff Nurse', 'Human Resources Assistant/Coordinator/Generalist', 'Residential Counselor', 'Clinician', 'Case Manager', 'Social Worker', 'Supervisor', 'Service Manager']:
        job_chosen = "Arts_Social_Sciences"
    
    if job_chosen in ['Freelance Designer', 'Marketing Specialist', 'Senior Design ', 'Engineer', 'Chief Engineer', 'Architectural Designer', 'Project Architect']:
        job_chosen = " "
    
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
            data.append([row[0],[row[1]],criteria,[row[3]], refs, row[5]])
        print(data)
        return render_template('6_courses_new.html', data=data, job_chosen=job_chosen)
    else:
        print("method: ", request.method)
        print('GET METHOD')
        print(db_name)
        descriptions = []
        for row in rows:
            descriptions.append(row[-3])
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

@app.route('/course_test/')
def courses():
    db = sqlite3.connect("uni_database_file/Data_car.db")
    cursor = db.execute(f"SELECT * FROM Business_Accounting")
    rows = cursor.fetchall()
    db.close()
    data = []
    for row in rows:
        criteria = row[2]
        criteria = criteria.split('-')
        refs = row[4]
        refs = refs.split("\n")
        data.append([row[0],[row[1]],criteria,[row[3]], refs])
    print(data)
    return render_template("6_courses_new.html", data=data)
    #return render_template('test_courses.html', data=data)


if __name__ == "__main__":
    run_once = 0
    if run_once == 0:
        set_default()
        run_once = 1
    app.run(debug=True)