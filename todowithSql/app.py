from flask import Flask, jsonify , json, render_template, session, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tasktodo.db'

database = SQLAlchemy(app)

class Todos(database.Model):
    id=database.Column(database.Integer , primary_key=True)
    title = database.Column(database.String(50))
    description = database.Column(database.String(200))
    done = database.Column(database.Boolean)



database.create_all()

@app.route('/task/musharraf/api/v1.0/todoapp' , methods=['GET'])
def get_todos():
    todo = Todos.query.all()

    output=[]
    for todos in todo:
        todos_data={}
        todos_data['id']=todos.id
        todos_data['title']=todos.title
        todos_data['description']=todos.description
        todos_data['done'] = todos.done
        output.append(todos_data)

    return jsonify({'result':output})

@app.route('/task/musharraf/api/v1.0/todoapp/<id>', methods=['GET'])
def one_todo(id):
    tods = Todos.query.filter_by(id=id).first()
    if not tods:
        return jsonify({'message':'Nothing in the dictionary'})

    todo_data = {}
    todo_data['id'] = tods.id
    todo_data['title'] = tods.title
    todo_data['description'] = tods.description
    todo_data['done'] = tods.done
    return jsonify(todo_data)

@app.route('/task/musharraf/api/v1.0/todoapp' , methods=['POST'])
def create_todos():
    data = request.get_json()

    todo =Todos(title=data['title'], description=data['description'], done=False)
    database.session.add(todo)
    database.session.commit()
    return jsonify ({'message':'Add sucessufully'})

@app.route('/task/musharraf/api/v1.0/todoapp/<id>', methods=['PUT'])
def update_todo(id):
    tods = Todos.query.filter_by(id=id).first()
    if not tods:
        return jsonify({'msg': 'Not found in the dictionary'})
    data = request.get_json()
    tods.done=True
    tods.title=data['title']
    tods.description=data['description']
    database.session.commit()
    return jsonify({'msg':'Sucessfully Update'})

@app.route('/task/musharraf/api/v1.0/todoapp/<int:todo_id>', methods=['DELETE'])
def todo_delete(todo_id):
    tods = Todos.query.filter_by(id=todo_id).first()
    if not tods:
        return jsonify({'msg': 'Not found in the dictionary'})
    else:
        database.session.delete(tods)
        database.session.commit()
    return jsonify({'msg':'Sucessfully deleted'})

app.run(debug=True ,port=8080)