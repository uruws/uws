#!/usr/bin/env python3

import sys

from subprocess import check_output

def _run(cmd):
	return check_output(cmd, shell = True, text = True)

def main():
	for line in _run('uwskube get nodes').splitlines():
		line = line.strip()
		if line.startswith('NAME'):
			continue
		host = line.split()[0]
		print(host, flush = True)
		show = False
		for info in _run(f"uwskube describe node {host}").splitlines():
			if info.startswith('Non-terminated Pods:'):
				show = True
				print(info, flush = True)
				continue
			if show:
				if not info.startswith(' '):
					break
				print(info, flush = True)
		print('', flush = True)
	return 0

if __name__ == '__main__':
	sys.exit(main())
