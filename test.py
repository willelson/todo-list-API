import unittest
from app import app, db, Task
import json

class FlaskTestCase(unittest.TestCase):

	def setUp(self):
		self.tester = app.test_client(self)
		app.config.from_object('config.TestingConfig')
	
	def tearDown(self):
		clear_tasks()

	def test_all_tasks_endpoint(self):
		clear_tasks()
		self.assertTrue(len(Task.query.all()) == 0)
		
		# Add a dummy task
		test = Task(title="test", description="does this work?")
		db.session.add(test)
		db.session.commit()

		response = self.tester.get('/tasks', content_type='html/text')

		# Check for dummy task in response
		self.assertTrue('"description": "does this work?"' in response.data)
		self.assertTrue('"title": "test"' in response.data)

	def test_task_endpoint(self):
		clear_tasks()
		self.assertTrue(len(Task.query.all()) == 0)
		
		# Add 2 dummy tasks
		test1 = Task(title="test1", description="abcdefg")
		test2 = Task(title="test2", description="hijklmnop")
		db.session.add(test1)
		db.session.add(test2)
		db.session.commit()

		response = self.tester.get('/task/{}'.format(test2.id), content_type='html/text')

		# Check for dummy task in response
		self.assertTrue('"description": "hijklmnop"' in response.data)
		self.assertTrue('"title": "test2"' in response.data)

	def test_create_task_endpoint(self):
		clear_tasks()
		self.assertTrue(len(Task.query.all()) == 0)
		
		response = self.tester.post('/task', data=json.dumps({'title':"Creation", 'description':"mmmbop"}),
									 content_type='application/json')

		# Check for dummy task in response
		self.assertTrue('"description": "mmmbop"' in response.data)
		self.assertTrue('"title": "Creation"' in response.data)

		test_task = Task.query.all()[0]
		self.assertTrue(test_task.title == "Creation")
		self.assertTrue(test_task.description == "mmmbop")

	def test_update_task_endpoint(self):
		clear_tasks()
		self.assertTrue(len(Task.query.all()) == 0)
		
		# Add 2 dummy tasks
		random_test = Task(title="test1", description="abcdefg")
		task_to_update = Task(title="test2", description="hijklmnop")
		db.session.add(random_test)
		db.session.add(task_to_update)
		db.session.commit()

		response = self.tester.put('/task/{}'.format(task_to_update.id), 
									data=json.dumps({'title':"New title", 'description':"I changed this"}),
									content_type='application/json')

		test_task = Task.query.filter_by(title="New title").first()
		self.assertTrue(test_task.title == "New title")
		self.assertTrue(test_task.description == "I changed this")


	def test_delete_task_endpoint(self):
		clear_tasks()
		self.assertTrue(len(Task.query.all()) == 0)
		
		# Add 2 dummy tasks
		random_task = Task(title="Random task", description="abcdefg")
		task_to_delete = Task(title="Delete Me", description="hijklmnop")
		db.session.add(random_task)
		db.session.add(task_to_delete)
		db.session.commit()

		response = self.tester.delete('/task/{}'.format(task_to_delete.id))
		
		updated_tasks = Task.query.all()

		self.assertTrue(len(updated_tasks) == 1)
		self.assertTrue(updated_tasks[0].title == "Random task")
		self.assertTrue(updated_tasks[0].description == "abcdefg")



def clear_tasks():
	tasks = Task.query.all()
	if len(tasks) > 0:
		for task in tasks:
			db.session.delete(task)
			db.session.commit()


if __name__ == '__main__':
	unittest.main()