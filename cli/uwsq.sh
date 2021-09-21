#!/bin/sh
set -eu
export NQDIR=/run/uwscli/nq
mkdir -p -m 0750 ${NQDIR}
cd ${NQDIR}
exec fq "$@"
