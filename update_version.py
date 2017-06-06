import re

filename = "app.py"
rep1 = "setup.py"
s = open(filename, "r").read()
version = s.split("__version__")[1].splitlines()[0].replace("=","").strip()
version = version.strip("\"").strip("\'")
s = open(rep1, "r").read()
#(\s*)=(\s*)
pattern = r"version(\s*)=(\s*)(\".+\"|\'.+\')"
result = re.search(pattern, s)
ns = re.sub(pattern, "version='%s'" % version, s)
open(rep1, "w").write(ns)