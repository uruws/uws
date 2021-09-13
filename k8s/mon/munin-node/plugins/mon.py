# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import math
import os
import re
import sys

from time import time

# logger

__debug = os.getenv('UWS_DEBUG', None)

def debug():
	return __debug

def log(*args):
	print(*args, file = sys.stderr)

def dbg(*args):
	if __debug:
		print('DEBUG: ', end = '', file = sys.stderr)
		log(*args)

# utils

__field_re = re.compile('\W')

def cleanfn(n):
	return __field_re.sub('_', n)

def derive(f):
	return math.ceil(f*1000)

# cache

__cachefn = '/tmp/mon.cache.nginx.stats'

def cacheSet(obj, fn = __cachefn):
	try:
		obj['__cache_expire'] = time() + 120
		with open(fn, 'w') as fh:
			json.dump(obj, fh)
			fh.close()
	except Exception as err:
		log(f"ERROR cacheSet{fn}:", err)

def cacheGet(fn = __cachefn):
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
