#!/usr/bin/env python3

import json
import os
import re
import sys

from time import time

__debug = os.getenv('UWS_DEBUG', None)
__nginx_metrics = 'http://metrics.ingress-nginx.svc.cluster.local:10254/metrics'
NGINX_METRICS_URL = os.getenv('NGINX_METRICS_URL', __nginx_metrics)

def log(*args):
	print(*args, file = sys.stderr)

def dbg(*args):
	if __debug:
		log(*args)

__field_re = re.compile('\W')

def cleanfn(n):
	return __field_re.sub('_', n)

def cacheSet(fn, obj, ttl = 120):
	try:
		obj['__cache_expire'] = time() + ttl
		with open(f"/tmp/mon.cache.{fn}", 'w') as fh:
			json.dump(obj, fh)
			fh.close()
	except Exception as err:
		log('ERROR cacheSet:', err)

def cacheGet(fn):
	obj = None
	try:
		with open(f"/tmp/mon.cache.{fn}", 'r') as fh:
			obj = json.load(fh)
			fh.close()
	except Exception as err:
		log('ERROR cacheGet:', err)
		dbg('cache miss')
		return None
	if obj is not None and time() >= obj['__cache_expire']:
		dbg('cache expired')
		return None
	dbg('cache hit')
	return obj
