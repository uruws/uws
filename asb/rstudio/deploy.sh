#!/bin/sh
set -eu
export SSH_KEYNAME=rstudio
./rstudio/vm-setup.sh $@ -t nginx
exec ~/asb/run.sh $@ ./rstudio/deploy.yaml
