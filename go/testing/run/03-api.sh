#!/bin/sh
set -eu

TMPDIR=/go/tmp/uwsapi
rm -rf ${TMPDIR}
install -d -m 0750 ${TMPDIR}

go test -coverprofile ${TMPDIR}/coverage.out ./cmd/uwsapi/... ./api/...

covd=${TMPDIR}/htmlcov
mkdir -p ${covd}

exec go tool cover -html ${TMPDIR}/coverage.out \
	-o ${covd}/coverage.html
