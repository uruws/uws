#!/bin/sh
set -eu
./rstudio/vm-setup.sh $@ -t nginx
exec ~/asb/run.sh $@ ./rstudio/deploy.yaml
