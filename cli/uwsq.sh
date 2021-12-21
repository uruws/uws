#!/bin/sh
set -eu
export NQDIR=/run/uwscli/nq
cd ${NQDIR}
exec fq "$@"
