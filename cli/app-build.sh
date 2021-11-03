#!/bin/sh
set -eu

app=${1:?'app name?'}
build_dir=${2:?'build dir?'}
build_script=${3:?'build script?'}
version=${4:?'version?'}

version_tag=$(echo "${version}" | tr '/' '_')

logs_dir=${HOME}/logs
logf=${logs_dir}/${app}-build-${version_tag}.log

mkdir -vp "${logs_dir}"
date -R >"${logf}"

build_cmd=${build_dir}/${build_script}
if test "$(dirname ${build_dir})" != '/srv/deploy'; then
	echo "ERROR: invalid cmd ${build_cmd}" | tee -a "${logf}"
	exit 9
fi

cd "${build_dir}"
git fetch --tags --prune --prune-tags | tee -a "${logf}"
git checkout "${version}" | tee -a "${logf}"

if ! test -x "./${build_script}"; then
	echo "[ERROR] build script not found: ./${build_script} (build dir: ${build_dir})" | tee -a "${logf}" >&2
	exit 8
fi

exec ./"${build_script}" | tee -a "${logf}"
