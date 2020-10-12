from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

database = "sqlite:///instructors.db"
instructor = Flask(__name__)
instructor.config["SQLALCHEMY_DATABASE_URI"] = database
db = SQLAlchemy(instructor)

@instructor.route('/')
def index():
    instructors = Instructor.query.all()
    return render_template("Index.html",instructors=instructors)
    

@instructor.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        id = request.form.get("id")
        title = request.form.get("title")
        firstname=request.form.get("firstname")
        lastname=request.form.get("lastname")
        link= request.form.get("link")
        #
        if link == "":
            read = ""
        else:
            read = "Read more about " + title + " " + firstname + " " + lastname
        
        instructor=Instructor(read = read, title=title,firstname=firstname,lastname=lastname,link=link)
        db.session.add(instructor)
        db.session.commit()
    
    instructors = Instructor.query.all()
    return render_template("Create.html",instructors=instructors) 

@instructor.route('/delete/<instructor_id>') # add id
def delete(instructor_id):
    #try:
    instructor = Instructor.query.get(instructor_id)
    db.session.delete(instructor)
    db.session.commit()
    instructors = Instructor.query.all()
    render_template("delete.html", instructors=instructors)
    return redirect('/')      

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(40), nullable = False)
    firstname=db.Column(db.String(40), nullable = False)
    lastname=db.Column(db.String(40), nullable = False)
    link = db.Column(db.String(180), nullable = True)
    read = db.Column(db.String(180), nullable = True)
    
    

if __name__ == '__main__':
    instructor.run(debug=True)