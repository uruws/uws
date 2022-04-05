#!/bin/sh
set -eu

sess=$(schroot -c uwscli-test -b)

cleanup() {
	schroot -c ${sess} -e
}

trap cleanup INT EXIT

schroot_sess="schroot -c ${sess} -r"

exec ${schroot_sess} -d /root -u root -- /bin/bash -i
