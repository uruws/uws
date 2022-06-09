#!/bin/sh
set -eu

app=${1:?'app name?'}
build_dir=${2:?'build dir?'}
build_script=${3:?'build script?'}
version=${4:?'version?'}

version_tag=$(echo "${version}" | tr '/' '_')

export UWSCLI_LOG=on
export UWSCLI_DEBUG=off

/srv/uws/deploy/cli/auth.py --user "${SUDO_USER}" --build "${app}"

logs_dir=${HOME}/logs
log_date=$(date '+%y%m%d-%H%M%S')
logf=${logs_dir}/${app}-build-${log_date}-${version_tag}.log

mkdir -vp "${logs_dir}"
date -R >"${logf}"

status_dir=/run/uwscli/build
statusf=${status_dir}/${app}.status

build_cmd=${build_dir}/${build_script}
if test "$(dirname ${build_dir})" != '/srv/deploy'; then
	echo "[ERROR] invalid cmd: ${build_cmd}" | tee -a "${logf}"
	exit 9
fi

echo "CHECK:${version}" >${statusf}
cd "${build_dir}"
git fetch --tags --prune --prune-tags | tee -a "${logf}"
git checkout "${version}" | tee -a "${logf}"

if ! test -x "./${build_script}"; then
	echo "[ERROR] build script not found: ./${build_script} (build dir: ${build_dir})" | tee -a "${logf}" >&2
	exit 8
fi

set +e

echo "BUILD:${version}" >${statusf}
./"${build_script}" | tee -a "${logf}"
rc=$?

if test "X${rc}" != 'X0'; then
	echo "FAIL:${version}" >${statusf}
else
	echo "OK:${version}" >${statusf}
	/srv/uws/deploy/cli/app-clean-build.sh "${app}"
	/srv/uws/deploy/cli/app-autobuild-deploy.sh "${app}" "${version}"
fi

exit ${rc}
