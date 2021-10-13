#!/bin/sh
set -eu
exec ansible-playbook $@ ./rstudio/deploy.yaml
