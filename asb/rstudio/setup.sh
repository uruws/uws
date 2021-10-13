#!/bin/sh
set -eu
exec ~/asb/run.sh \
	./rstudio/ec2-key.yaml \
	./rstudio/ec2-vpc.yaml
