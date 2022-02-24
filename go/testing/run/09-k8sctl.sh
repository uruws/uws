#!/bin/sh
set -eu

TMPDIR=/go/tmp/k8sctl
rm -rf ${TMPDIR}
install -d -m 0750 ${TMPDIR}

export UWS_CLUSTER=k8stest

go test -coverprofile ${TMPDIR}/coverage.out ./cmd/k8sctl/... ./k8s/ctl/...

covd=${TMPDIR}/htmlcov
mkdir -p ${covd}

exec go tool cover -html ${TMPDIR}/coverage.out \
	-o ${covd}/coverage.html
