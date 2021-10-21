#!/bin/sh
set -eu
exec ~/asb/run.sh $@ ./kali/ec2-vm-check.yaml
