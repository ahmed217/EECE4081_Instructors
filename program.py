from flask import Flask
from flask import render_template
from flask import request
from flask import redirect


# install using,  pip3 install sqlalchemy flask-sqlalchemy 
from flask_sqlalchemy import SQLAlchemy

# this is the database connection string or link 
# brokenlaptops.db is the name of database and it will be created inside 
# project directory. You can choose any other direcoty to keep it, 
# in that case the string will look different. 
database = "sqlite:///brokenlaptops.db"


app = Flask(__name__)

# important configuration parameter, don't miss it 
app.config["SQLALCHEMY_DATABASE_URI"] = database

# database instance. thid db will be used in this project 
db = SQLAlchemy(app)

##################################################
# use python shell to create the database (from inside the project directory) 
# >>> from app import db
# >>> db.create_all()
# >>> exit()
# if you do not do this step, the database file will not be created and you will receive an error message saying "table does not exist".
###################################################

@app.route('/')
def index():
    instructor = Instructor.query.all()
    return render_template("index.html",instructor=instructor)
    

@app.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        ID=request.form.get("ID")
        instructor = Instructor(firstname=firstname,lastname=lastname,ID=ID)
        db.session.add(instructor)
        db.session.commit()
    
    instructor = Instructor.query.all()
    return render_template("create.html",instructor=instructor)    
    # now add two lines to retrieve all the BrokenLaptop from the database and display 
    # as it is done in '/' index route 
    
    
@app.route('/delete/<laptop_id>') # add id
def delete(laptop_id):
    brokenlaptop = Instructor.query.get(laptop_id)
    db.session.delete(brokenlaptop)
    db.session.commit()
    # add a line of code to commit the delete operation 
     
    
    brokenlaptops = Instructor.query.all()
    return render_template("delete.html",brokenlaptops=brokenlaptops)  
    # now add two lines to retrieve all the BrokenLaptop from the database and display 
    # as it is done in '/' index route 
    
@app.route('/update/<laptop_id>', methods=['GET','POST']) # add id 
def update(laptop_id):
    if request.form:
        newbrand = request.form.get("brand")
        newprice = request.form.get("price")
        
        brokenlaptop = Instructor.query.get(laptop_id)
        brokenlaptop.brand = newbrand
        brokenlaptop.price = newprice
        # in this block, a modified instance of BrokenLaptop is coming in along with id
        # add few lines of code so that the modification is saved in the database 
        # for example, Brand of a laptop should be updated from 'Dell' to 'Dell Latitude'
        # code snippet will be similar to create() method 
        db.session.commit()
        return redirect("/")

    brokenlaptop = Instructor.query.get(laptop_id)
    return render_template("update.html",brokenlaptop=brokenlaptop)
    # now adde two lines to retrive all the BrokenLaptop from the database and display 
    # as it is done in '/' index route 

# this class creates a table in the database named broken_laptop with 
# entity fields id as integer, brand as text, and price as decimal number 
# create a module containing this class and import that class into this application and use it
class Instructor(db.Model):
    ID = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(40), nullable = False)
    lastname = db.Column(db.Float, nullable = True)
    

if __name__ == '__main__':
    app.run(debug=True)