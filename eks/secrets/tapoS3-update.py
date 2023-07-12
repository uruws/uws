#!/usr/bin/env python3

import json
import sys

from argparse import ArgumentParser
from pathlib  import Path

__doc__ = 'secret tapoS3 credentials updater'

def getCredentials(env):
	f = Path('./secret/aws.iam/tapoS3%s_accessKeys.csv' % env)
	i = f.read_text().splitlines()[-1].strip().split(',')
	return (i[0].strip(), i[1].strip())

def writeSettings(fn, key, secret):
	f = Path(fn)
	print(f)
	with f.open() as fh:
		obj = json.load(fh)
	try:
		bucket = obj['amazon']['bucket']
		curkey = obj['amazon']['key']
		cursec = obj['amazon']['secret']
	except KeyError as err:
		print('key error:', err)
		return 2
	obj['amazon']['key'] = key
	obj['amazon']['secret'] = secret
	with f.open('w') as fh:
		json.dump(obj, fh, sort_keys = True, indent = 4)
	return 0

def main(argv):
	flags = ArgumentParser(description = __doc__)
	flags.add_argument('env', help = 'tapoS3 env')
	flags.add_argument('json', help = 'meteor settings json file')
	args = flags.parse_args(argv)
	rc = 0
	try:
		key, secret = getCredentials(args.env)
		rc = writeSettings(args.json, key, secret)
	except FileNotFoundError as err:
		print(err)
		return 1
	return rc

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
