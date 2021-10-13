#!/bin/sh
set -eu
alias asbpl=ansible-playbook
asbpl ./rstudio/ec2-key.yaml
asbpl ./rstudio/ec2-vm.yaml
exit 0
