#!/usr/bin/env python3

import sys

from argparse import ArgumentParser
from pathlib  import Path

__doc__ = 'secret uwsadm credentials updater'

def getCredentials():
	f = Path('./secret/aws.iam/uwsadm_accessKeys.csv')
	i = f.read_text().splitlines()[-1].strip().split(',')
	return (i[0].strip(), i[1].strip())

def genConfig(key, secret):
	f = Path('./secret/aws/credentials')
	print(f)
	with f.open('w') as fh:
		fh.write('[default]\n')
		fh.write('aws_access_key_id = %s\n' % key)
		fh.write('aws_secret_access_key = %s\n' % secret)
		fh.write('\n')
		fh.write('[uwsadm]\n')
		fh.write('aws_access_key_id = %s\n' % key)
		fh.write('aws_secret_access_key = %s\n' % secret)

def main(argv):
	flags = ArgumentParser(description = __doc__)
	args = flags.parse_args(argv)
	try:
		key, secret = getCredentials()
		genConfig(key, secret)
	except FileNotFoundError as err:
		print(err)
		return 1
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
