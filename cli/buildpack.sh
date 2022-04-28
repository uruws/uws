#!/bin/sh
set -eu

src=${1:?'app src?'}
target=${2:?'build target?'}
version=${3:?'build version?'}

/srv/uws/deploy/cli/auth.py --user "${SUDO_USER}" --build "${target}"

/srv/uws/deploy/cli/uwsnq.sh -- "${SUDO_USER}" /srv/deploy/Buildpack/build.py \
	--src "${src}" --target "${target}" --version "${version}"

exit 0
