#!/usr/bin/env python3

import sys
import yaml

from argparse import ArgumentParser
from pathlib  import Path

__doc__ = 'k8s nginx ingress deploy helper'

K8S_VERSION = '1.22'
UPSTREAM    = f"./k8s/nginx-ingress/{K8S_VERSION}/upstream-deploy.yaml"

def _setup(docs):
	for d in docs:
		if d['kind'] == 'Deployment':
			continue
		elif d['kind'] == 'Job':
			continue
		print('---', file = sys.stdout)
		yaml.dump(d, sys.stdout)

def _setup_jobs(docs):
	for d in docs:
		if d['kind'] == 'Job':
			print('---', file = sys.stdout)
			yaml.dump(d, sys.stdout)

def _deploy(f, args):
	with f.open() as fh:
		docs = yaml.safe_load_all(fh)
		if args.setup:
			_setup(docs)
		elif args.setup_jobs:
			_setup_jobs(docs)
		else:
			for d in docs:
				if d['kind'] == 'Deployment':
					if args.replicas > 0:
						d['spec']['replicas'] = args.replicas
					print('---', file = sys.stdout)
					yaml.dump(d, sys.stdout)
					break
	return 0

def main(argv):
	flags = ArgumentParser(description = __doc__)

	flags.add_argument('-f', '--filename', metavar = 'upstream', default = UPSTREAM,
		help = 'upstream yaml definition file')
	flags.add_argument('-r', '--replicas', metavar = 'int', default = 0,
		help = 'nginx controller replicas', type = int)

	flags.add_argument('-D', '--deploy', action = 'store_true', default = False,
		help = 'ingress deploy')
	flags.add_argument('-J', '--setup-jobs', action = 'store_true', default = False,
		help = 'ingress setup jobs')
	flags.add_argument('-S', '--setup', action = 'store_true', default = False,
		help = 'ingress setup')

	args = flags.parse_args(argv)

	f = Path(args.filename)
	if not f.exists():
		print(f"{f}: file not found", file = sys.stderr)
		return 9

	return _deploy(f, args)

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
