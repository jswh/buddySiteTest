#!/usr/bin/python
# Filename : test.py

import json
f = file('testcases', 'r')
lines = f.readlines()
line = lines[13]
subs = line.split('info:')
jsn = json.loads(subs[1])

