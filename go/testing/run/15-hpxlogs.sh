#!/bin/sh
set -eu

TMPDIR=/go/tmp/hpxlogs
rm -rf ${TMPDIR}
install -d -m 0750 ${TMPDIR}

go test -coverprofile ${TMPDIR}/coverage.out ./cmd/hpxlogs/... ./hpxlogs/...

covd=${TMPDIR}/htmlcov
mkdir -p ${covd}

go tool cover -html ${TMPDIR}/coverage.out -o ${covd}/coverage.html
exit 0
