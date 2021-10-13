#!/bin/sh
set -eu
exec ansible-playbook $@ ./rstudio/ec2-vm-check.yaml
