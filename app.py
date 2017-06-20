import flask
from flask import request, jsonify, session
import sqlalchemy
from sqlalchemy import inspect, desc
import json
import models
from models import engine, dbsession

__author__ = "Prahlad Yeri"
__license__ = "MIT"
__credits__ = ["Prahlad Yeri"]
__version__ = "1.0.11"
__status__ = "Production"

app = flask.Flask(__name__)

#TODO: move this to a configuration file.
config = {
	'auth': False #enable authentication.
	}

def is_login_valid():
	return session.get('auth_email') != None

@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def index():
	return "It Works!"

@app.route("/_info")
def info():
	return jsonify({
		"Application": "flask-tiddly %s" % __version__,
		"Powered By": "flask %s, sqlalchemy %s" % (flask.__version__, sqlalchemy.__version__),
		})
		
@app.route("/login", methods=["POST"])
def login():
	data = request.get_json(force=True)
	data = json.loads(data)
	print('data:',data, type(data))
	query = dbsession.query(models.User).filter_by(email=data['email'], password=data['password'])
	rows = query.all()
	if len(rows) == 0:
		return jsonify({'status':'error', 'error':'Invalid email or password.'})
	else:
		session['auth_email'] = rows[0].email
		return jsonify({'status':'success'})

@app.route("/<table_name>", methods=["GET", "POST", "PUT", "DELETE", "FETCH"])
def fetch(table_name):
	print("verb: %s, tablename: %s" % (request.method, table_name))
	if config['auth'] and not is_login_valid():
		print("Unauthorized Access.")
		return jsonify({
				"status": "error",
				"error": "Unauthorized Access."
			})
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
				"status": "success",
				"data": data
				})
		except Exception as e:
			return jsonify({
				"status": "error",
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
				"status": "success",
				"id": object.id,
				})
		except Exception as e:
			return jsonify({
				"status": "error",
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
				"status": "success",
				"id": object.id,
				})
		except Exception as e:
			return jsonify({
				"status": "error",
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
			
			query = dbsession.query(TableClass).filter_by(**data['where'])
			if 'orderby' in data:
				for cname in data['orderby'].split(','):
					reverse = False
					if cname.endswith(' desc'):
						reverse = True
						cname = cname[:-5]
					elif cname.endswith(' asc'):
						cname = cname[:-4]
					print("cname: ", cname)
					column = getattr(TableClass, cname)
					if reverse: column = desc(column)
					query = query.order_by(column)
			if 'limit' in data:
				query = query.limit(data['limit'])
				query = query.offset(data['offset'])
			object = query.all()
			data = [object_as_dict(t) for t in object]
			return jsonify({
				"status": "success", 
				"data": data
				})
		except Exception as e:
			return jsonify({
				"status": "error",
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
	print("tiddly v%s" % __version__)
	app.secret_key = "4d5ert54fgcdf587ed5d"
	app.debug = True
	app.run()