#!/bin/sh
set -eu
export SSH_KEYNAME=rstudio
exec ~/asb/run.sh $@ \
	./rstudio/ec2-vm.yaml \
	./rstudio/ec2-vm-check.yaml \
	./rstudio/vm-setup.yaml
