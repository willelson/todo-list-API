from flask import Flask, jsonify, request, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper

app = Flask(__name__)
db = SQLAlchemy(app)

SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

def serialize(model):
  """
  Transforms a model into a dictionary which can be dumped to JSON.
  """
  columns = [c.key for c in class_mapper(model.__class__).columns]
  return dict((c, getattr(model, c)) for c in columns)

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	description = db.Column(db.String(120))
	done = db.Column(db.Boolean)

	def __init__(self, **kwargs):
		super(Task, self).__init__(**kwargs)
		self.done = False

	def __repr__(self):
		return self.title


@app.route('/tasks', methods=["GET"])
def tasks():
	"""
	Return all tasks
	"""
	# Serialize each task and return in JSON 
	tasks = Task.query.all()
	serialized_tasks = [serialize(task)for task in tasks]
	return jsonify({"tasks":serialized_tasks})



@app.route('/task/<task_id>', methods=["GET"])
def task(task_id):
	"""
	Return a specific task
	"""
	task = Task.query.get(task_id)
	return jsonify(serialize(task))

@app.route('/task', methods=["POST"])
def create_task():
	# If request not in json format or doesn't contain a title return a bad request error
	if not request.json or not 'title' in request.json:
		abort(400)

	task = Task(title=request.json['title'])
	if 'description' in request.json:
		task.description = request.json['description']
	if 'done' in request.json:
		task.done = request.json['done']

	db.session.add(task)
	db.session.commit()

	# respond to client with task added and code 201 which means Created
	return jsonify(serialize(task)), 201


@app.errorhandler(404)
def not_found(error):
	"""Return 404 error in JSON rather then HTML"""
	return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/task/<task_id>', methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'Deletion': 'succesful'}), 200


@app.route('/task/<task_id>', methods=['PUT'])
def update_task(task_id):
	task = Task.query.get(task_id)

	if task is None:
		abort(404)

	if not request.json:
		abort(400)
	if 'title' in request.json and type(request.json['title']) != unicode:
		abort(400)
	if 'description' in request.json and type(request.json['description']) is not unicode:
		abort(400)
	if 'done' in request.json and type(request.json['done']) is not bool:
		abort(400)

	if 'title' in request.json:
		task.title = request.json['title']
	if 'description' in request.json:
		task.description = request.json['description']
	if 'done' in request.json:
		task.done = request.json['done']

	db.session.add(task)
	db.session.commit()

	return jsonify(serialize(task))


if __name__ == "__main__":
	app.run(debug=True, port=5000)









"""
http://stackoverflow.com/questions/14920080/how-to-create-sqlalchemy-to-json
"""