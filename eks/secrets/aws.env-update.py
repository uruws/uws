#!/usr/bin/env python3

import sys

from argparse import ArgumentParser
from pathlib  import Path

__doc__ = 'secret aws.env credentials updater'

def getCredentials(name):
	f = Path('./secret/aws.iam/%s_accessKeys.csv' % name)
	i = f.read_text().splitlines()[-1].strip().split(',')
	return (i[0].strip(), i[1].strip())

def genConfig(name, key, secret):
	f = Path('./secret/aws.env', name, 'credentials')
	print(f)
	with f.open('w') as fh:
		fh.write('# %s\n' % name)
		fh.write('[default]\n')
		fh.write('aws_access_key_id = %s\n' % key)
		fh.write('aws_secret_access_key = %s\n' % secret)

def main(argv):
	flags = ArgumentParser(description = __doc__)
	flags.add_argument('name', help = 'aws.env name')
	args = flags.parse_args(argv)
	try:
		key, secret = getCredentials(args.name)
		genConfig(args.name, key, secret)
	except FileNotFoundError as err:
		print(err)
		return 1
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
