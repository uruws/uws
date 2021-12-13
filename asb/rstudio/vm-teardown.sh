#!/bin/sh
set -eu
exec ~/asb/run.sh "$@" ./rstudio/ec2-vm-teardown.yaml
