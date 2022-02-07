#!/bin/sh
set -eu

prof=uwscli

sess=$(schroot -c ${prof} -b)

cleanup() {
	schroot -c ${sess} -e
}

trap cleanup INT EXIT

schroot_sess="schroot -c ${sess} -r"

${schroot_sess} -d /srv/deploy/uws -- /srv/deploy/uws/cli/schroot/entrypoint.sh

exit 0
