from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__) #creates flask application object
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app) #initialize database and bind it to flask application

class ToDo(db.Model): #Model is a base class from SQLAlchemy that the class ToDo inherits from
    id=db.Column(db.Integer, primary_key=True) #id acts as primary key giving unique index for each item
    content = db.Column(db.String(200), nullable=False) #nullable=false says that content cant be left blank
    data_created=db.Column(db.DateTime, default=datetime.utcnow) #typo here data instead of date created however when I tried to change it and run it showed that database didnt have a date created column
    #in order to change column name we will have to go to terminal and make chnages to database using db.create_all() which we used when making the database or import flask migrate and perform some steps

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET']) #@app.route is a flask decorator that maps a URL (here / that represents local host link we use) to index function
#GET is default method, when we go to local host url browser sends a GET request to flask app/server and this calls the index func which returns html file
#POST method can be used to send data (user fills form) to the server (flask server handles and processes requests and generates responses) which updates database and refreshes the page
def index():
    if request.method == 'POST':
        task_content=request.form['content']
        new_task=ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    else:
        tasks= ToDo.query.order_by(ToDo.data_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting the task"

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task= ToDo.query.get_or_404(id)

    if request.method == 'POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error updating the task'
    else:
        return render_template('update.html', task=task)

if __name__=="__main__" : #ensures app is run only when script run directly (not as a module)
    app.run(debug=True)