import requests, json

#obj = {"where": {"text":"foob", "id":1}}
#obj = {"where": {"id":1}}
#obj = {"where": {"text":"test data"}}
obj = {"where": {"name":"admin"}, "orderby": "email desc", "limit":2, "offset": 2}
#print(json.dumps(obj))
#exit()
print("sending request")
#res = requests.get('http://localhost:5000/dual/1', json=json.dumps(obj))

sess = requests.session()
#res = sess.request('POST', 'http://localhost:5000/login', json=json.dumps({'email':'linus@expo.com','password':'confused'}))
res = sess.request('FETCH', 'http://localhost:5000/user', json=json.dumps(obj))

#res = requests.post('http://localhost:5000/dual', json={"text":"chai and biscuit."})
#res = requests.post('http://localhost:5000/dual', json={"text":"test data"})
#res = requests.put('http://localhost:5000/dual/5', json={"text":"ram chip."})
#res = requests.post('http://localhost:5000/user', json={"email":"foobar@nowhere.com", "password":"confused"})
#res = requests.post('http://localhost:5000/user', json={"name": "admin", "email":"linus@expo.com", "password":"confused"})
#res = requests.put('http://localhost:5000/user/2', json={"email":"doodle@nowhere.com", "password":"doodle"})
# res = requests.delete('http://localhost:5000/dual/1')
# res = requests.delete('http://localhost:5000/dual/2')
# res = requests.delete('http://localhost:5000/dual/4')
if res.ok:
	# print(res.json())
	d = res.json()
	if 'data' in d:
		for li in d['data']:
			print(li)
	else:
		print(d)
