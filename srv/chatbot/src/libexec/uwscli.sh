#!/bin/sh
set -eu
hostname=${1:?'hostname?'}
username=${2:?'username?'}
shift
shift
exec /usr/bin/ssh -a -C -n -x -o BatchMode=yes -l "${username}" "${hostname}" "$@"
