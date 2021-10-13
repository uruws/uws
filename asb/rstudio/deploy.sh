#!/bin/sh
set -eu
export SSH_KEYNAME=rstudio
exec ~/asb/run.sh ./rstudio/deploy.yaml
