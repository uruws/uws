# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import math
import os
import re
import sys

from time import time

# logger

_debug = os.getenv('UWS_DEBUG', None) is not None

def debug():
	return _debug

def _print(*args, end = os.linesep):
	print(*args, end = end, file = sys.stderr)

def log(*args):
	_print(*args)

def dbg(*args):
	if _debug:
		_print('DEBUG: ', end = '')
		log(*args)

# utils

__field_re = re.compile('\W')

def cleanfn(n):
	return __field_re.sub('_', n)

def derive(f):
	return math.ceil(f*1000)

__cluster = os.getenv('UWS_CLUSTER', None)

def cluster():
	return __cluster

def color(n):
	c = n + 1
	if c > 28:
		c = 0
	return c

def generateName(pod):
	n = None
	m = pod['metadata']
	l = m.get('labels', {})
	gn = m.get('generateName', None)
	if gn:
		ph = l.get('pod-template-hash', None)
		if ph:
			n = gn.replace(f"-{ph}-", "", 1)
		else:
			n = gn
	if n.endswith('-'):
		n = n[:-1]
	return n

def containerImage(n):
	return n.split('/')[-1].strip()

# cache

def __cachefn(fn):
	fn = cleanfn(fn)
	return f"/tmp/mon.{fn}.cache"

def cacheSet(obj, fn):
	fn = __cachefn(fn)
	try:
		obj['__cache_expire'] = time() + 120
		with open(fn, 'w') as fh:
			json.dump(obj, fh)
			fh.close()
	except Exception as err:
		log(f"ERROR cacheSet{fn}:", err)

def cacheGet(fn):
	fn = __cachefn(fn)
	obj = None
	try:
		with open(fn, 'r') as fh:
			obj = json.load(fh)
			fh.close()
	except Exception as err:
		log(f"ERROR cacheGet {fn}:", err)
		dbg('cache miss')
		return None
	if obj is not None and time() >= obj['__cache_expire']:
		dbg('cache expired')
		return None
	dbg('cache hit')
	return obj
