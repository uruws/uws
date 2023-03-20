#!/bin/sh
set -eu

TMPDIR=/go/tmp/ngxlogs
rm -rf ${TMPDIR}
install -d -m 0750 ${TMPDIR}

go test -coverprofile ${TMPDIR}/coverage.out ./cmd/ngxlogs/... ./ngxlogs/...

covd=${TMPDIR}/htmlcov
mkdir -p ${covd}

go tool cover -html ${TMPDIR}/coverage.out -o ${covd}/coverage.html
exit 0
