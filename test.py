import requests

#res = requests.post('http://localhost:5000/dual', json={"text":"chai and biscuit."})
#res = requests.post('http://localhost:5000/dual', json={"text":"computer chip."})
#res = requests.put('http://localhost:5000/dual/5', json={"text":"ram chip."})
#res = requests.post('http://localhost:5000/user', json={"email":"foobar@nowhere.com", "password":"confused"})
#res = requests.put('http://localhost:5000/user/2', json={"email":"doodle@nowhere.com", "password":"doodle"})
res = requests.delete('http://localhost:5000/dual/5')
if res.ok:
	print(res.json())