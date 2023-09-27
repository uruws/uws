# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import os.path
import subprocess
import sys

from argparse import ArgumentParser

def main(argv = []):
	parser = ArgumentParser()
	parser.add_argument('--profile', help = 'aws credentials profile',
		default = os.getenv('AWS_PROFILE', 'uwsdev'))
	parser.add_argument('--region', help = 'aws region',
		default = os.getenv('AWS_REGION', 'us-west-2'))
	parser.add_argument('--zones', help = 'aws region zones')
	parser.add_argument('--nodes', help = 'desired number of nodes',
		type = int, default = 2)
	parser.add_argument('--nodes-min', help = 'min number of nodes',
		type = int, default = 2)
	parser.add_argument('--nodes-max', help = 'max number of nodes',
		type = int, default = 2)
	parser.add_argument('--max-pods-per-node', help = 'max number of pods per node',
		type = int, default = 0)
	parser.add_argument('--instance-types', help = 'instance types', default = 't2.small')
	parser.add_argument('--k8s-version', help = 'kubernetes version', default = '1.19')
	parser.add_argument('--fargate', help = 'setup fargate nodes', action = 'store_true')
	parser.add_argument('--spot', help = 'create managed spot nodegroup', default = 'false')
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
	cmd = 'eksctl -v %s create cluster --name %s' % (args.v, args.name)
	cmd += ' --profile %s' % args.profile
	if args.region is not None:
		cmd += ' --region %s' % args.region
	if args.zones is not None:
		cmd += ' --zones %s' % args.zones
	cmd += ' --tags uwseks=%s' % args.name
	cmd += ' --version %s' % args.k8s_version
	if args.fargate:
		cmd += ' --fargate'
		if args.max_pods_per_node > 0:
			cmd += ' --max-pods-per-node %d' % args.max_pods_per_node
	else:
		cmd += ' --managed'
		cmd += ' --asg-access'
		if args.spot.strip() == 'true':
			cmd += ' --spot'
	cmd += ' --nodegroup-name main'
	cmd += ' --nodes %d' % args.nodes
	cmd += ' --nodes-min %d' % args.nodes_min
	cmd += ' --nodes-max %d' % args.nodes_max
	cmd += ' --instance-types %s' % args.instance_types
	cmd += ' --ssh-access'
	node_ssh_key = os.path.expanduser('~/secret/ssh/%s/node.pub' % args.name)
	cmd += ' --ssh-public-key %s' % node_ssh_key
	cmd += ' --full-ecr-access'
	cmd += ' --auto-kubeconfig'
	return cmd
