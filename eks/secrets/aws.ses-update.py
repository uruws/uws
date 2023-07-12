#!/usr/bin/env python3

import sys

from argparse   import ArgumentParser
from pathlib    import Path
from subprocess import getoutput

__doc__ = 'secret aws.ses smtps credentials updater'

def getCredentials():
	f = Path('./secret/aws.iam/smtps_credentials.csv')
	i = f.read_text().splitlines()[-1].strip().split(',')
	return (i[1].strip(), i[2].strip())

def gitFiles(grep):
	cmd = '/usr/bin/git grep -El %s' % grep
	return getoutput(cmd).splitlines()

def shUpdate(fn, key, secret):
	f = Path(fn)
	content = f.read_text()
	with f.open('w') as fh:
		for line in content.splitlines():
			if line.startswith('UWS_SMTPS_USER='):
				fh.write('UWS_SMTPS_USER=%s\n' % key)
			elif line.startswith('UWS_SMTPS_PASSWD='):
				fh.write('UWS_SMTPS_PASSWD=%s\n' % secret)
			else:
				fh.write('%s\n' % line)

def msmtprcUpdate(key, secret):
	f = Path('./secret/eks/files/mailx/aws.ses/msmtprc')
	print(f)
	content = f.read_text()
	with f.open('w') as fh:
		for line in content.splitlines():
			if line.startswith('user AKIA'):
				fh.write('user %s\n' % key)
				fh.write('password %s\n' % secret)
			elif line.startswith('password '):
				continue
			else:
				fh.write('%s\n' % line)

def main(argv):
	flags = ArgumentParser(description = __doc__)
	args = flags.parse_args(argv)
	try:
		key, secret = getCredentials()
	except FileNotFoundError as err:
		print(err)
		return 1
	# sh files
	for fn in gitFiles('^UWS_SMTPS_USER='):
		print(fn)
		shUpdate(fn, key, secret)
	# msmtprc
	try:
		msmtprcUpdate(key, secret)
	except FileNotFoundError as err:
		print(err)
		return 2
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
