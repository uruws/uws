#!/usr/bin/env python3

import fileinput
import sys

def main(args):
	for line in fileinput.input('-'):
		print(line)
	return 128

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
