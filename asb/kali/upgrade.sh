#!/bin/sh
set -eu
exec ~/asb/run.sh "$@" ./kali/upgrade.yaml
