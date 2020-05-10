from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())


    def __str__ (self):
        return f'Task {self.id}'


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    salary = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())


    def __str__ (self):
        return f'Task {self.id}'


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "something went wrong"
    else:    
        all_tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('home.html', all_tasks=all_tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return ("something went wrong")


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return redirect("something went wrong")
    else:
        return render_template("taskEdit.html", task=task)


@app.route('/api/users')
def getUsers():
    all_users = [x.as_dict() for x in Users.query.order_by(Users.created_at).all()]
    return jsonify(all_users)


@app.route('/user', methods=["POST", "GET"])
def users():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        salary = request.form["salary"]
        new_user = Users(name=name, location=location, salary=salary)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/user')
        except:
            return "something went wrong"
    else:
        return render_template("newUser.html")


# to create database open python from curent directory 
# from app import db
# db.create_all()

if __name__ == "__main__":
    app.run(debug=True)