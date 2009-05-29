#!/usr/bin/python

import operator
import glob
import re
import pprint
import math

# find all the files in this directory
files = glob.glob('./*/*/*')

TESTS=(
  # name, regex, category, weight, reverse
  ('integer bit', re.compile('integer bit: ([\w,.]+)'), 'cpu', 1, False),
  ('integer add', re.compile('integer add: ([\w,.]+)'), 'cpu', 1, False),
  ('integer mul', re.compile('integer mul: ([\w,.]+)'), 'cpu', 1, False),
  ('integer div', re.compile('integer div: ([\w,.]+)'), 'cpu', 1, False),
  ('integer mod', re.compile('integer mod: ([\w,.]+)'), 'cpu', 1, False),
  ('float add', re.compile('float add: ([\w,.]+)'), 'cpu', 1, False),
  ('float mul', re.compile('float mul: ([\w,.]+)'), 'cpu', 1, False),
  ('float div', re.compile('float div: ([\w,.]+)'), 'cpu', 1, False),
  ('double add', re.compile('double add: ([\w,.]+)'), 'cpu', 1, False),
  ('double mul', re.compile('double mul: ([\w,.]+)'), 'cpu', 1, False),
  ('double div', re.compile('double div: ([\w,.]+)'), 'cpu', 1, False),
  ('Simple read', re.compile('Simple read: ([\w,.]+)'), 'disk', 1, False),
  ('Simple write', re.compile('Simple write: ([\w,.]+)'), 'disk', 1, False),
  ('Simple stat', re.compile('Simple stat: ([\w,.]+)'), 'disk', 1, False),
  ('file write bandwidth', re.compile('File /var/tmp/XXX write bandwidth: ([\w,.]+)'), 'disk', 3, True),
  ('MHZ', re.compile('\[MHZ: (\d+)'), 'cpu', 0.4, True),
  ('MB', re.compile('\[MB: (\d+)'), 'mem', .3, True),
)
data = {}
for test in TESTS:
  data[test[0]] = {}

for file in files:
  data[file] = {}
  for line in open(file).readlines():
    for test in TESTS:
      match = test[1].match(line)
      if match:
        data[test[0]][file] = (float(match.groups()[0]), test[3], test[4])
      else:
        pass

results = {}
ranks = len(files)

for test in TESTS:
  type = test[2]
  if not results.has_key(type):
    results[type] = {}
    
  places = sorted(data[test[0]].iteritems(), key=operator.itemgetter(1), reverse=test[4])
  for i in range(ranks):
    try:
      if not results[type].has_key(places[i][0]):
        results[type][places[i][0]] = 0
      results[type][places[i][0]] += (ranks - i) * (ranks - i*.25)* test[3] # multiply by weight
    except IndexError:
      pass

# foo
# disk **
# cpu ***
indiv = {}
for result in results:
  places = sorted(results[result].iteritems(), key=operator.itemgetter(1), reverse=True)
  max = float(places[0][1])
  for place in places:
    if not indiv.has_key(place[0]):
      indiv[place[0]] = {}
    if not indiv[place[0]].has_key('total'):
      indiv[place[0]]['total'] = 0
      
    indiv[place[0]][result] = float(place[1] / max) * 5
    indiv[place[0]]['total'] += float(place[1])

for host in indiv:
  print host
  for bm in indiv[host]:
    if bm == 'total':
      continue
    print '\t%-5s %s' % (bm, '*'*int(indiv[host][bm]))

#for host in indiv.iteritems():
#  print host[0],
#  print ','.join([str(v) for v in host[1].values()])
