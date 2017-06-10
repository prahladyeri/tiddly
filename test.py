import requests, json

obj = {"where": {"text":"foob", "id":50}}
#obj = {"where": {"id":1}}
#print(json.dumps(obj))
#exit()
print("sending request")
#res = requests.get('http://localhost:5000/dual/1', json=json.dumps(obj))
res = requests.request('FETCH', 'http://localhost:5000/dual', json=json.dumps(obj))
#res = requests.post('http://localhost:5000/dual', json={"text":"chai and biscuit."})
#res = requests.post('http://localhost:5000/dual', json={"text":"computer chip."})
#res = requests.put('http://localhost:5000/dual/5', json={"text":"ram chip."})
#res = requests.post('http://localhost:5000/user', json={"email":"foobar@nowhere.com", "password":"confused"})
#res = requests.put('http://localhost:5000/user/2', json={"email":"doodle@nowhere.com", "password":"doodle"})
# res = requests.delete('http://localhost:5000/dual/1')
# res = requests.delete('http://localhost:5000/dual/2')
# res = requests.delete('http://localhost:5000/dual/4')
if res.ok:
	print(res.json())