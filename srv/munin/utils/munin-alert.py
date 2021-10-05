#!/usr/bin/env python3

import fileinput
import sys

def main(args):
	try:
		for line in fileinput.input('-'):
			print(line)
	except KeyboardInterrupt:
		return 1
	return 128

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
