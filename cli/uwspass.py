#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
sys.path.insert(0, '/srv/home/uwscli/lib')

from argparse import ArgumentParser
from getpass  import getpass
from hashlib  import pbkdf2_hmac

import uwscli
import uwscli_user

__salt = b'K0mP2LvwSIPnCI_hyqmEaeRN4_hHiQ1PC_ohAf1J6Eh3FAhD'

def main(argv):
	uwscli.debug('start')

	flags = ArgumentParser(description = __doc__)
	flags.add_argument('-V', '--version', action = 'version',
		version = uwscli.version())
	flags.add_argument('-u', '--user', help = 'user name', required = True)

	args = flags.parse_args(argv)

	user = uwscli.user_get(args.user.strip())
	if user is None:
		uwscli.error('invalid user:', args.user)
		return 8

	uid = uwscli.user_uuid(user.username)
	fn = '/run/uwscli/auth/%s/password' % uid

	pw = getpass(prompt = 'New Password:')
	pw2 = getpass(prompt = 'Repeat new Password:')
	if pw != pw2:
		uwscli.error('password do not match')
		return 9
	h = pbkdf2_hmac('sha256', pw.encode(), __salt, 100000).hex()

	with open(fn, 'w') as fh:
		print(h, file = fh)

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
