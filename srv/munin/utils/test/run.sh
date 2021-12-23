#!/bin/sh
set -eu
export PYTHONPATH=${HOME}/utils/lib:${HOME}/utils/test
script=${1}
shift
exec ${script} $@
