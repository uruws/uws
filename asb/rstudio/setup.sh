#!/bin/sh
set -eu
alias asbpl=ansible-playbook
asbpl ./rstudio/ec2-key.yaml
asbpl ./rstudio/ec2-security-group.yaml
exit 0
