#!/usr/bin/env python3

import sys

from argparse import ArgumentParser
from pathlib  import Path

__doc__ = 'secret gen for amazon eks cluster'

def getCredentials(profile):
	f = Path('./secret/aws.iam/%s_accessKeys.csv' % profile)
	i = f.read_text().splitlines()[-1].strip().split(',')
	return (i[0].strip(), i[1].strip())

def genAdmin(cluster, profile, key, secret):
	f = Path('./secret/eks/aws/admin', cluster, 'credentials')
	print(f)
	with f.open('w') as fh:
		fh.write('[default]\n')
		fh.write('aws_access_key_id = %s\n' % key)
		fh.write('aws_secret_access_key = %s\n' % secret)
		fh.write('\n')
		fh.write('[%s]\n' % profile)
		fh.write('aws_access_key_id = %s\n' % key)
		fh.write('aws_secret_access_key = %s\n' % secret)
		fh.close()

def genClient(cluster, profile):
	key, secret = getCredentials('uwscli')
	f = Path('./secret/eks/aws/client', cluster, 'credentials')
	print(f)
	with f.open('w') as fh:
		fh.write('[default]\n')
		fh.write('aws_access_key_id = %s\n' % key)
		fh.write('aws_secret_access_key = %s\n' % secret)
		fh.write('\n')
		fh.write('[%s]\n' % profile)
		fh.write('aws_access_key_id = %s\n' % key)
		fh.write('aws_secret_access_key = %s\n' % secret)
		fh.close()

def main(argv):
	flags = ArgumentParser(description = __doc__)

	flags.add_argument('-p', '--profile', required = True, help = 'cluster iam profile')
	flags.add_argument('name', help = 'cluster name')

	args = flags.parse_args(argv)

	try:
		key, secret = getCredentials(args.profile)
		genAdmin(args.name, args.profile, key, secret)
		genClient(args.name, args.profile)
	except FileNotFoundError as err:
		print(err)
		return 1

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
