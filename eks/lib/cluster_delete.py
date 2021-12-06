# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys
import subprocess

from argparse import ArgumentParser

def main(argv = []):
	parser = ArgumentParser()
	parser.add_argument('--profile', help = 'aws credentials profile',
		default = os.getenv('AWS_PROFILE', 'uwsdev'))
	parser.add_argument('--region', help = 'aws region',
		default = os.getenv('AWS_REGION', 'us-west-2'))
	parser.add_argument('--wait', help = 'wait tasks to finish', action = 'store_true')
	parser.add_argument('-v', help = 'verbose level', default = '3')
	parser.add_argument('name', help = 'cluster name')
	args = parser.parse_args(argv)
	cmd = _createCluster(args)
	print(cmd)
	try:
		subprocess.run(cmd, shell = True, check = True)
	except Exception:
		return 1
	return 0

def _createCluster(args):
	cmd = 'eksctl -v %s delete cluster --name %s' % (args.v, args.name)
	cmd += ' --profile %s' % args.profile
	if args.region is not None:
		cmd += ' --region %s' % args.region
	if args.wait:
		cmd += ' --wait'
	return cmd
