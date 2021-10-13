#!/bin/sh
set -eu
ansible-playbook $@ ./rstudio/ec2-vm.yaml
exec ./rstudio/ec2-vm-check.sh
