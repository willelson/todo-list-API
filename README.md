# Todo list API

This project is 


### Install and run

Install the requirements 
```
pip install requirements.txt
```
Once the dependencies are installed we can set up the database system. I'm using Postgres but there's no reason you couldn't use an alternative such as sqlite. If you decide to use the [Postgres app](http://postgresapp.com), once you have that installed you can create a new database for this application from the terminal.
```
createdb <YOUR-DATABASE-NAME>
```
You will then need to head into the config file and update `SQLALCHEMY_DATABASE_URI` to match your newly created database. Then run the python script to populate the database with the model tables defined in this application.

```
python db_create.py
```

Run the flask application and start making calls to the API.
```
python app.py
```
You could check everything is working by making a call from the terminal to add a task
```
curl -i -H "Content-Type: application/json" -X POST -d '{"title":"New task"}' http://127.0.0.:5000/task
```


## Running the tests

The unit tests are written using the python unittest module. To run them:
```
python test.py
```

## Built With

* [Python 2.7](http://www.python.org/) - The progamming language used.
* [Flask](http://flask.pocoo.org) - The web framework used.
* [Postgres](https://www.postgresql.org) - The Database system implemented.


## Authors
* **Will Elson** - [GitHub](https://github.com/willelson) - [email](mailto:elson594@gmail.com)

See also the list of [contributors](https://github.com/willelson/todo-list-API/contributors) who participated in this project.

## License

This project is licensed under the MIT License 