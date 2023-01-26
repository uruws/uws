#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json
import sys

from dataclasses import dataclass

__doc__ = 'k8s upgrades helper'

@dataclass
class Config(object):
	docker_tag: str = ''
	eks_tag:    str = ''
	k8s_tag:    str = ''

cfg: dict[str, Config] = {
	'1.22': Config(
		docker_tag = '2211',
		eks_tag    = '122',
		k8s_tag    = '122',
	),
	'1.25': Config(
		docker_tag = '2211',
		eks_tag    = '125',
		k8s_tag    = '125',
	),
}

def main(argv: list[str]) -> int:
	print(cfg)
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
