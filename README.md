![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)
[![](https://www.paypalobjects.com/en_US/i/btn/x-click-but04.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JM8FUXNFUK6EU)

# Flask-Tiddly

##### Table of Contents

1. [What is flask-tiddly](#what-is)
2. [Project Details](#project-details)
7. [Installation](#installation)
3. [Feature Roadmap](#feature-roadmap)
11. [License](#license)
13. [Stack](#stack)

## What is Flask-Tiddly

`flask-tiddly` is a minimal, prototype RESTful server app for basic CRUD transactions. It is database agnostic and uses sqlalchemy on the backend to talk to RDBMS. The database is `sqlite` by default, but you can switch to anything you want by making this small change in the `models.py`:

	engine = create_engine("sqlite:///tiddly.db", echo=True)
	Base = declarative_base()

## Project Details

You can host this app and use it as your own replacement for any cloud based database such as firebase or CouchDB as long as you follow the CRUD based I/O approach. The RESTful methods are versatile and compatible with the data needs of typical Single Page Apps developed in Angular or Backbone. For example:

	GET  	/books ..... => Get all rows from the books table.
	POST 	/books ..... => Insert record into books table from posted JSON data.
	GET  	/books/1 ... => Fetch the book record where the `id` field equals `1`.
	PUT  	/books/1 ... => Update the record where `id` equals `1` with posted JSON data.
	DELETE  /books/1 ... => Delete the record where `id` equals `1`.
	
The only "opinionated" thing about this app is this dependence on the `id` field. It assumes that each table has `id` column defined as the primary key and the CRUD transactions are based on that. Also, additional tables like `books` in this example need to be defined in `models.py`. By default, `flask-tiddly` comes with only two tables called `dual` and `user` to play around.

## Installation

To install and run this project, just clone/download this github directory and start the `tiddly` app:

	python app.py
	
I've tested this on Python 3.6, but it should ideally run on other versions too. Once you run it, you can open your browser and browse the following `url` to make sure its running:

	http://127.0.0.1:5000
	
After that, you can make the following POST request to insert some data into the dual table.

	requests.post('http://localhost:5000/dual', json={"text":"chai and biscuit."})

You can use the accompanying `test.py` or any other tool like `curl` to make these requests. Now, open up the browser again and visit below `url` to list all the records in the `dual` table:

	http://127.0.0.1:5000/dual
	
After running the above command, you should be able to see something like this:

	{
	  "data": [
		{
		  "id": 1, 
		  "text": "chai and biscuit."
		}
	  ], 
	  "status": "success", 
	  "verb": "GET"
	}
	
Similarly, you can try out the other verbs - `PUT` and `DELETE` to update and delete records respectively. To create your own new table, open the `models.py` in a text-editor and define your own class based on the sqlalchemy declarative `Base` class. Write the new class code around the other defined Model classes, for example the `Dual` class:

	class Dual(Base):
		__tablename__ = "dual"
		id = Column(Integer, primary_key=True)
		text = Column(String)
		
		def repr(self):
			return "<Dual(id=%s, text=%s, )>" % (id, text)
			
Finally, you can also install `flask-tiddly` using `pip` just to play around with:

	pip install tiddly
			
## Feature Roadmap

I intend to add the following features to this template project soon:

- User sign-in and authentication using token key or session.
- Advanced querying using `where` and `order by` clauses.
- Fetching summaries using `group by` clauses.
- Enhanced security and error handling.

## License

flask-tiddly is free and open source and available under `MIT` license.

## Stack

`tlask-tiddly` is built using the robust `flask` framework and `sqlalchemy` library.