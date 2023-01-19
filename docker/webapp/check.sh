#!/bin/sh
set -eu
webapp=${1:?'webapp name?'}
exec ./docker/webapp/cmd.sh "${webapp}" /usr/local/bin/webapp-check.sh
