#!/bin/sh
set -eu
envname="${1:?'env name?'}"
exec docker stop "uwsapi-${envname}"
