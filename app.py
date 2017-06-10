import flask
from flask import request, jsonify
import sqlalchemy
from sqlalchemy import inspect
import json
import models
from models import engine, dbsession

__author__ = "Prahlad Yeri"
__license__ = "MIT"
__credits__ = ["Prahlad Yeri"]
__version__ = "1.0.9"
__status__ = "Production"

app = flask.Flask(__name__)

@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def index():
	return "It Works!"

@app.route("/_info")
def info():
	return jsonify({
		"Application": "flask-tiddly %s" % __version__,
		"Powered By": "flask %s, sqlalchemy %s" % (flask.__version__, sqlalchemy.__version__),
		})
		
@app.route("/_query/<table_name>", methods=["FETCH"])
def query(table_name):
	print("verb: %s, table: %s" % (request.method, table_name))
	if request.method == "FETCH":
		try:
			data = request.get_json(force=True)
			data = json.loads(data)
			print("data: ", data)
			print("data-type: ", type(data))
			TableClass = models.get_class_by_tablename(table_name)
			if TableClass == None: raise Exception("Table not found: %s" % table_name)
			object = dbsession.query(TableClass).filter_by(**data['where']).all()
			data = [object_as_dict(t) for t in object]
			return jsonify({
				"status": "success", "verb": request.method,
				"data": data
				})
		except Exception as e:
			return jsonify({
				"status": "error", "verb": request.method,
				"error": str(e),
				})

@app.route("/<table_name>", defaults={"id":None}, methods=["GET", "POST", "PUT", "DELETE", "FETCH"])
@app.route("/<table_name>/<id>", methods=["GET", "POST", "PUT", "DELETE", "FETCH"])
def fetch(table_name, id):
	print("verb: %s, table: %s, id: %s" % (request.method, table_name, id))
	if request.method == "GET":
		try:
			TableClass = models.get_class_by_tablename(table_name)
			if TableClass == None: raise Exception("Table not found: %s" % table_name)
			if id == None: #all data
				object = dbsession.query(TableClass).all()
				data = [object_as_dict(t) for t in object]
			else:
				object = dbsession.query(TableClass).filter_by(**{"id":id}).first()
				if object == None: raise Exception("No data found.")
				data = object_as_dict(object)
			return jsonify({
				"status": "success", "verb": request.method,
				"data": data
				})
		except Exception as e:
			return jsonify({
				"status": "error", "verb": request.method,
				"error": str(e),
				})
	elif request.method == "POST" or request.method == "PUT":
		data = request.get_json(force=True)
		print("data:", data)
		try:
			TableClass = models.get_class_by_tablename(table_name)
			if TableClass == None: raise Exception("Table not found: %s" % table_name)
			if request.method == "POST": #insert data
				object = TableClass(**data)
				dbsession.add(object)
				dbsession.commit()
			else: #update data
				object = dbsession.query(TableClass).filter_by(**{"id":id}).first()
				if object == None: raise Exception("No data found.")
				#object.update(**data)
				for key in data.keys():
					setattr(object, key, data[key])
				#dbsession.add(object)
				dbsession.commit()
			return jsonify({
				"status": "success", "verb": request.method,
				"id": object.id,
				})
		except Exception as e:
			return jsonify({
				"status": "error", "verb": request.method,
				"error": str(e),
				})
	elif request.method == "DELETE":
		try:
			TableClass = models.get_class_by_tablename(table_name)
			if TableClass == None: raise Exception("Table not found: %s" % table_name)
			object = dbsession.query(TableClass).filter_by(**{"id":id}).first()
			if object == None: raise Exception("No data found.")
			dbsession.delete(object)
			dbsession.commit()
			return jsonify({
				"status": "success", "verb": request.method,
				"id": object.id,
				})
		except Exception as e:
			return jsonify({
				"status": "error", "verb": request.method,
				"error": str(e),
				})
	elif request.method == "FETCH":
		try:
			data = request.get_json(force=True)
			data = json.loads(data)
			print("data: ", data)
			print("data-type: ", type(data))
			TableClass = models.get_class_by_tablename(table_name)
			if TableClass == None: raise Exception("Table not found: %s" % table_name)
			object = dbsession.query(TableClass).filter_by(**data['where']).all()
			data = [object_as_dict(t) for t in object]
			return jsonify({
				"status": "success", "verb": request.method,
				"data": data
				})
		except Exception as e:
			return jsonify({
				"status": "error", "verb": request.method,
				"error": str(e),
				})
	else:
		return jsonify({
			"status": "error", "error": "Unrecognized verb.",
			})
			
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

if __name__ == "__main__":
	app.secret_key = "4d5ert54fgcdf587ed5d"
	app.debug = True
	app.run()