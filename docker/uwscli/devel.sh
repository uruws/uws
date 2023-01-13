#!/bin/sh
set -eu

CLI_HOME=${PWD}/host/assets/jsbatch/srv/home/uwscli

mkdir -vp ${PWD}/tmp/uwscli ${PWD}/tmp/uwscli_rundir \
	${PWD}/tmp/uwscli/pytest_cache
mkdir -vp ${CLI_HOME}/vendor/semver-2.13.0/.pytest_cache

exec docker run -it --rm --name uwscli-devel \
	--hostname clidev.uws.local \
	-e PYTHONPATH=/srv/home/uwscli/lib:/srv/home/uwscli/vendor/semver-2.13.0 \
	-v ${CLI_HOME}/bin:/srv/home/uwscli/bin:ro \
	-v ${CLI_HOME}/etc:/srv/home/uwscli/etc:ro \
	-v ${CLI_HOME}/lib:/srv/home/uwscli/lib:ro \
	-v ${CLI_HOME}/vendor:/srv/home/uwscli/vendor:rw \
	-v ${PWD}/secret/cli:/srv/uws/deploy/secret/cli:ro \
	-v ${PWD}/cli:/srv/uws/deploy/cli:ro \
	-v ${PWD}/cli/test:/home/uws/test:ro \
	-v ${PWD}/cli/testdata:/home/uws/testdata:ro \
	-v ${PWD}/tmp/uwscli_rundir:/run/uwscli:rw \
	-v ${PWD}/tmp/uwscli:/home/uws/tmp:rw \
	-v ${PWD}/tmp/uwscli/pytest_cache:/srv/home/uwscli/vendor/semver-2.13.0/.pytest_cache:rw \
	uws/cli-2211 "$@"
