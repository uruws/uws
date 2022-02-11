#!/bin/sh
set -eu
/srv/uws/deploy/cli/auth.py --user "${SUDO_USER}" --build "${UWS_BUILD_APP}"
exec /srv/deploy/Buildpack/build.py "$@"
