from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_wtf import FlaskForm


app = Flask(__name__)




app.config['MONGO_DBNAME'] = 'student'
app.config['MONGO_URI'] = 'mongodb://musharraf:yousuf1@ds117422.mlab.com:17422/student'
mongo = PyMongo(app)




@app.route("/task/musharraf/api/v1.0/todoapp", methods=['GET'])
def index():
    allData = mongo.db.todo_app.find()
    return render_template('index.html',todo=allData)






@app.route("/task/musharraf/api/v1.0/todoapp/edit/<id>", methods=['GET'])
def update(id):
    todos = mongo.db.todoapp.find_one({"_id": ObjectId(id)})
    return render_template('update.html', todos=todos,id=id)


@app.route("/task/musharraf/api/v1.0/todoapp", methods=['POST', 'GET'])
def addTodo():

    
    users = mongo.db.todo_app
    title = request.form['title']
    desc = request.form['description']
    done = bool(title and desc)
    users.insert({'title': request.form['title'],
                 'description': request.form['description'], 'done': done})
    allData = mongo.db.todo_app.find()
    
    return render_template('index.html',todo=allData)


@app.route("/task/musharraf/api/v1.0/todoapp/<id>")
def delete(id):
    users = mongo.db.todo_app
    uid = users.find_one({"_id": ObjectId(id)})
    print(uid)
    users.remove(uid, True)
    return redirect(url_for('index'))


@app.route("/task/musharraf/api/v1.0/todoapp/update/<id>", methods=['POST'])
def edit(id):
    users = mongo.db.todo_app
    uid = users.find_one({"_id": ObjectId(id)})
    title = request.form['title']
    Description = request.form['desc']
    

    uid['title'] = title
    uid['description'] = Description
    uid['done'] = True
    users.save(uid)
    return redirect(url_for('index'))







app.run(debug=True, use_reloader=False)
