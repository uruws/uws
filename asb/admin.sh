#!/bin/sh
set -eu
asbenv=${1:?'ansible env?'}
exec ./docker/asb/run.sh ${asbenv}
