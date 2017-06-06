from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper
import json

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
	# Serialize each task and return in JSON 
	tasks = Task.query.all()
	serialized_tasks = [serialize(task)for task in tasks]
	return jsonify({"tasks":serialized_tasks})



if __name__ == "__main__":
	app.run(debug=True, port=5000)









"""
http://stackoverflow.com/questions/14920080/how-to-create-sqlalchemy-to-json
"""