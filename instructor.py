from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
import json
from flask import jsonify

database = "sqlite:///instructors.db"
instructor = Flask(__name__)
instructor.config["SQLALCHEMY_DATABASE_URI"] = database
db = SQLAlchemy(instructor)

@instructor.route('/')
def index(): 
    instructors = Instructor.query.all()
    return render_template("Index.html",instructors=instructors)
    
@instructor.route('/json')
def createJson():
    instructors = Instructor.query.all()
    #return json.dumps(instructors)
    return jsonify( json_list =[i.serialize() for i in instructors])
@instructor.route("/about", methods=['GET','POST'])
def about():
    return render_template("about.html")
@instructor.route("/contact", methods=['GET','POST'])
def contact():
    return render_template("contact.html")
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

@instructor.route('/update/<instructor_id>', methods=['GET','POST']) # add id 
def update(instructor_id):
    if request.form:
        newtitle = request.form.get("title")
        newfirstname = request.form.get("firstname")
        newlastname  = request.form.get("lastname")
        newlink = request.form.get("link")
        
        instructor = Instructor.query.get(instructor_id)
        instructor.title = newtitle
        instructor.firstname = newfirstname
        instructor.lastname = newlastname
        instructor.link = newlink

        
        db.session.commit() 
        
        return redirect("/")
    instructors = Instructor.query.all()
        
    instructor = Instructor.query.get(instructor_id)
    return render_template('update.html', instructor = instructor, title= "Update an Instructor", instructors = instructors)
"""
it gets the instructor's id and simply recreates the id line
from the new title name and link, it replaces the old title name and link
it redirects to "/"
"""


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
    
    def serialize(self):
        return {
                'Title'        :   self.title,
                'First Name'     :   self.firstname,
                'Last Name'     :   self.lastname,
        }
    
    

if __name__ == '__main__':
    instructor.run(debug=True)