#!/bin/sh
set -eu
exec ansible-playbook $@ \
	./rstudio/ec2-key.yaml \
	./rstudio/ec2-vpc.yaml
