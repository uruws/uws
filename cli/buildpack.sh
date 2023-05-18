#!/bin/sh
set -eu

src=${1:?'app src?'}
target=${2:?'build target?'}
version=${3:?'build version?'}
autodeploy=${4:-False}

export UWSCLI_LOG=on
export UWSCLI_DEBUG=off

/srv/uws/deploy/cli/auth.py --user "${SUDO_USER}" --build "${target}"

/srv/uws/deploy/cli/uwsnq.sh "${SUDO_USER}" /srv/deploy/Buildpack/build.py \
	--src "${src}" --target "${target}" --version "${version}"

/srv/uws/deploy/cli/uwsnq.sh "${SUDO_USER}" \
	/srv/uws/deploy/cli/app-clean-build.sh "${target}"

if test 'XTrue' = "X${autodeploy}"; then
	/srv/uws/deploy/cli/uwsnq.sh "${SUDO_USER}" \
		/srv/uws/deploy/cli/app-autobuild-deploy.sh "${target}" "${version}"
fi

exit 0
