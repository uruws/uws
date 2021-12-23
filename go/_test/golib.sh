#!/bin/sh
set -eu

TMPDIR=/go/tmp/golib
install -d -m 0750 ${TMPDIR}

go test -coverprofile ${TMPDIR}/coverage.out ./log/...

covd=${TMPDIR}/htmlcov
mkdir -p ${covd}

go tool cover -html ${TMPDIR}/coverage.out -o ${covd}/coverage.html
exit 0
