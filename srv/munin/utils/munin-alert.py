#!/usr/bin/env python3

import fileinput
import json
import sys

def parse(stats):
	print('STATS:', stats)

def main():
	# ~ fh = open('/home/uws/tmp/munin-run/alerts.out', 'w')
	try:
		for line in fileinput.input('-'):
			line = line.strip()
			# ~ print(line, file = fh)
			try:
				# ~ print('LINE:', line)
				stats = json.loads(line)
			except Exception as err:
				# TODO: send [ERROR] by email
				print('ERROR:', err, file = sys.stderr)
				continue
			parse(stats)
	except KeyboardInterrupt:
		# ~ fh.close()
		return 1
	# ~ fh.close()
	return 128

if __name__ == '__main__':
	sys.exit(main())
