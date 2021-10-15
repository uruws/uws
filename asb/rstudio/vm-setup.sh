#!/bin/sh
set -eu
~/asb/run.sh ./rstudio/ec2-vm.yaml
exec ./rstudio/check.sh
