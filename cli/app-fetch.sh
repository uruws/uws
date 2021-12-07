#!/bin/sh
set -eu
workdir=${1:?'workdir?'}
exec git -C "${workdir}" fetch --prune --prune-tags --tags
