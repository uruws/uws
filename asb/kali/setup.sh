#!/bin/sh
set -eu
exec ~/asb/run.sh $@ \
	./kali/ec2-key.yaml \
	./kali/ec2-vpc.yaml
