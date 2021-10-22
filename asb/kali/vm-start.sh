#!/bin/sh
set -eu
~/asb/run.sh $@ ./kali/ec2-vm-start.yaml
exec ./kali/check.sh $@
