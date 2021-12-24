#!/bin/sh
set -eu

TMPDIR=/go/tmp/k8smon
rm -rf ${TMPDIR}
install -d -m 0750 ${TMPDIR}

export CGO_ENABLED=0
export UWS_CLUSTER=k8stest

go test -coverprofile ${TMPDIR}/coverage.out ./cmd/k8smon/... ./k8s/mon/...

covd=${TMPDIR}/htmlcov
mkdir -p ${covd}

go tool cover -html ${TMPDIR}/coverage.out -o ${covd}/coverage.html
exit 0
