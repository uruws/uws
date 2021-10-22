#!/bin/sh
set -eu
exec ~/asb/run.sh $@ \
	./kali/ec2-vm.yaml \
	./kali/ec2-vm-check.yaml \
	./kali/upgrade.yaml \
	./kali/vm-setup.yaml
