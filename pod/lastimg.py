#!/usr/bin/env python3

import json
import sys

from os         import environ
from semver     import compare
from subprocess import check_output

def main(argv = []):
	image = argv[0].strip()
	if image == '':
		print('[ERROR]: no image name provided', file = sys.stderr)
		return 9
	profile = environ.get('AWS_PROFILE', 'NO_AWS_PROFILE')
	region = environ.get('AWS_REGION', 'NO_AWS_REGION')
	cmd = f"aws ecr list-images --profile {profile} --region {region} --repository-name uws --output json"
	il = json.loads(check_output(cmd, shell = True))
	ver_max = None
	for img in il.get('imageIds', []):
		tag = img.get('imageTag', 'NO_imageTag').strip()
		if tag.startswith(f"{image}-"):
			ver = tag.replace(f"{image}-", '', 1)
			if ver_max is None:
				ver_max = ver
			else:
				if compare(ver, ver_max) == 1:
					ver_max = ver
	print(ver_max)
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
