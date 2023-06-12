# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import math
import os
import re
import sys

from time import time

def system(cmd) -> int:
	return os.system(cmd) >> 8

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
	if isinstance(f, str):
		return f
	return math.ceil(f*1000)

_cluster = os.getenv('UWS_CLUSTER', None)

def cluster():
	return _cluster

def color(n):
	c = n + 1
	if c > 28:
		c = 0
	return c

def generateName(pod):
	n = None
	m = pod.get('metadata', {})
	l = m.get('labels', {})
	gn = m.get('generateName', None)
	if gn:
		ph = l.get('pod-template-hash', None)
		if ph:
			n = gn.replace(f"-{ph}-", "", 1)
		else:
			n = gn
	if n is not None and n.endswith('-'):
		n = n[:-1]
	return n

def containerImage(n):
	return n.split('/')[-1].strip()

# cache

def _cachefn(fn):
	fn = cleanfn(fn)
	return f"/tmp/mon.{fn}.cache"

def _openfn(fn, mode):
	return open(fn, mode)

def _jsonDump(obj, fh):
	json.dump(obj, fh)

def _jsonLoad(fh):
	return json.load(fh)

def cacheSet(obj, fn):
	fn = _cachefn(fn)
	try:
		obj['__cache_expire'] = time() + 120
		with _openfn(fn, 'w') as fh:
			_jsonDump(obj, fh)
	except Exception as err:
		log(f"ERROR cacheSet{fn}:", err)

def cacheGet(fn):
	fn = _cachefn(fn)
	obj = None
	try:
		with _openfn(fn, 'r') as fh:
			obj = _jsonLoad(fh)
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
