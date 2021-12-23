#!/bin/sh
set -eu

TMPDIR=/go/tmp/uwsbot
rm -rf ${TMPDIR}
install -d -m 0750 ${TMPDIR}

export CGO_ENABLED=0
go test -coverprofile ${TMPDIR}/coverage.out ./cmd/uwsbot/... ./bot/...

covd=${TMPDIR}/htmlcov
mkdir -p ${covd}

go tool cover -html ${TMPDIR}/coverage.out -o ${covd}/coverage.html
exit 0
