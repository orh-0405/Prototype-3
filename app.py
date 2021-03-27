from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True)