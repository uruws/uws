#!/bin/sh
set -eu
exec ~/asb/run.sh "$@" ./rstudio/upgrade.yaml
