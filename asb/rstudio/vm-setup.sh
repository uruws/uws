#!/bin/sh
set -eu
exec ~/asb/run.sh "$@" \
	./rstudio/ec2-vm.yaml \
	./rstudio/ec2-vm-check.yaml \
	./rstudio/vm-setup.yaml
