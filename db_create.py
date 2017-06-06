from app import db, Task

db.create_all()

first_task = Task(title="Set up db", 
				  description="Get Postgres up and running!")

db.session.add(first_task)
db.session.commit()

