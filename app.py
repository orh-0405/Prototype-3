from flask import Flask, render_template, request
import os.path
import sqlite3

curr_dir = os.path.dirname(__file__)

def get_db(db_name):
    db_file_name = os.path.join(curr_dir, db_name)
    db = sqlite3.connect(db_file_name, check_same_thread=False) #db, db3, sqlite, sqlite3
    print("Opened database successfully")#;
    db.row_factory = sqlite3.Row
    return db

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

@app.route('/get_jobs/<string:personality>/')
def get_jobs(personality):
    New_db_name = 'uni_database_file/' + personality + '_car' + '.db'
    print(New_db_name)
    db = get_db(New_db_name)
    cursor = db.execute("SELECT * FROM Jobs_Avail")
    rows = cursor.fetchall()
    data = []
    for row in rows:
        jobs = row[2].split("\n")
        data.append([row[1], jobs])
    return render_template('4_job_options.html', data=data)


@app.route('/job_info/<string:job_chosen>/<string:db_name>/', methods = ['POST', 'GET'])
def job_info(job_chosen, db_name):
    print("HERE job info")
    New_db_name = 'uni_database_file/' + db_name + '.db'
    db = get_db(New_db_name)
    print("JOb: ", job_chosen)
    cursor = db.execute(f"SELECT * FROM {job_chosen}")
    rows = cursor.fetchall()
    if request.method == "POST":
        print("POST METHOD")
        data = []
        for row in rows:
            #final = ""
            criteria = row[2]
            criteria = criteria.split('-')
            criteria[2] = criteria[0] + " " + criteria[1] + " " + criteria[2]
            refs = row[4]
            refs = refs.split("\n")
            data.append([row[0],[row[1]],criteria[2:],[row[3]], refs])
        print(data)
        return render_template('6_course.html', data=data)
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

@app.route('/test/')
def test():
    return render_template('test.html')


@app.route('/courses/')
def courses():
    return render_template('6_course.html')


@app.route('/chat_with_profs/')
def chat_with_profs():
    return render_template('chatwithprof_sec.html')


if __name__ == "__main__":
    app.run(debug=True)
