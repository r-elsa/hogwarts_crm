from flask import Flask, jsonify,render_template, request, redirect, url_for
import random, string, time

app = Flask(__name__,template_folder='templates_')

students = [
            {
            'id': '1',
            'fname':'Harry',
            'lname':'Potter',
            'creation': time.ctime(),
            'imgurl':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYEiXw9Fg9vlRYRQuKGk2jTB1O7z37FCa9G-coNf8jizYutoWgdg&s',
            'lupdate': time.ctime(),
            'emskills':[{"skill":"Alchemy", "level":"5"}],
            'dmskills':[{"skill":"Conjuror", "level":"3"}],
            'dcourse': ["Alchemy advanced", "Magic for day-to-day life"]
            },
            {
             'id': '2',
             'fname':'Hermoine',
             'lname':'Granger',
             'creation':time.ctime(),
             'imgurl':'https://vignette.wikia.nocookie.net/harry-potter-what-should-have-been/images/3/34/Hermione_Granger.jpg/revision/latest?cb=20180606004557',
             'lupdate': time.ctime(),
             'emskills':[{"skill":"Alchemy", "level":"5"}],
             'dmskills':[{"skill":"Conjuror", "level":"3"}],
             'dcourse':["Alchemy advanced","Magic for day-to-day life"]
   
            },
                 {
             'id': '3',
             'fname':'Ron',
             'lname':'Weasley',
             'creation':time.ctime(),
             'imgurl':'https://i.pinimg.com/originals/c0/16/8b/c0168b9d3246351ef051d05c1cc7fd88.jpg',
             'lupdate': time.ctime(),
             'emskills':[{"skill":"Possession", "level":"5"}],
             'dmskills':[{"skill":"Elemental", "level":"5"}],
             'dcourse':["Alchemy advanced","Magic for day-to-day life"]
   
            }

]

magic_skills = ["Alchemy","Animation", "Conjuror","Disintegration","Elemental", "Healing","Illusion","Immortality","Invisibility","Invulnerability","Necromancer","Omnipresent","Omniscient","Poison","Possession","Self-detonation","Summoning","Water breathing"]

dcourse = ["Alchemy basics","Alchemy advanced","Magic for day-to-day life","Magic for medical professionals","Dating with magic"]

def generate_id():
    randomId = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(5)]) 
    return randomId


@app.route('/students', methods=['GET', 'POST'])
def getstudents():
    if request.method =='POST':
        student = {'fname': request.json['fname']}
        students.append(student)
        return render_template("students.html", students= students)
    else:
         return render_template("students.html", students= students)



@app.route('/students/dashboard')
def dashboard():
     return render_template("dashboard.html", students= students)


@app.route('/')
def root():
    return redirect(url_for("getstudents"))


@app.route('/students/<string:fname>', methods=['GET'])
def getstudent(fname):
    student = {}
    if request.method =='GET':
        for student in students:
            if student['fname']== fname:
                student_ = student
            
    return render_template("student.html", student = student_ )
    
###########################################################    
@app.route("/students/<string:fname>/edit", methods=['GET', 'POST'])
def edit_student(fname):
   
    if request.method =='GET':
        student = {}
        for student in students:
            if student['fname'] == fname:
                student_ = student     
                return render_template("editstudent.html", student = student_ )
    
    elif request.method == 'POST':
        student = {}
        for student in students:
            if student['fname'] == fname:
                student = student 
                student['fname'] = request.form['fname']
                student['imgurl'] = request.form['imgurl']
                student['id'] = generate_id()
                student['lname'] = request.form['lname']
                student['creation'] = request.form['creation']
                student['lupdate'] = time.ctime()
                
                
                emskills = request.form.getlist('emskills')
                emskills = [{'skill': emskill} for emskill in emskills]
                emskills_level = request.form.getlist('emskills_level')
                for i in range(len(emskills)):
                    emskills[i]["level"] = emskills_level[i]
                student['emskills'] = emskills

                dmskills = request.form.getlist('dmskills')
                dmskills = [{'skill': dmskill} for dmskill in dmskills]
                dmskills_level = request.form.getlist('dmskills_level')
                for i in range(len(dmskills)):
                    dmskills[i]["level"] = dmskills_level[i]
                student['dmskills'] = dmskills

                courses = []
                courses = request.form.getlist('dcourse')
                student['dcourse'] = courses

                return redirect(url_for("getstudents"))
 
 

@app.route("/addstudent", methods=['POST','GET'])
def add_student():
    student = {}
    if request.method =='POST':
        student['fname'] = request.form['fname']
        student['imgurl'] = request.form['imgurl']
        student['id'] = generate_id()
        student['lname'] = request.form['lname']
    
        student['creation'] = time.ctime()
        student['lupdate']= time.ctime()
      
      
        emskills = request.form.getlist('emskills')
        emskills = [{'skill': emskill} for emskill in emskills]
        emskills_level = request.form.getlist('emskills_level')
        for i in range(len(emskills)):
            emskills[i]["level"] = emskills_level[i]
        student['emskills'] = emskills

        dmskills = request.form.getlist('dmskills')
        dmskills = [{'skill': dmskill} for dmskill in dmskills]
        dmskills_level = request.form.getlist('dmskills_level')
        for i in range(len(dmskills)):
            dmskills[i]["level"] = dmskills_level[i]
        student['dmskills'] = dmskills

        courses = []
        courses = request.form.getlist('dcourse')
        student['dcourse'] = courses

    
        students.append(student)
        return redirect(url_for("getstudents"))
    else:
        return render_template("addstudent.html")


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r  

if __name__ == "__main__":
    app.run(debug=True,port=5000)