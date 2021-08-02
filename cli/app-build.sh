#!/bin/sh
set -eu

build_dir=${1:?'build dir?'}
build_script=${2:?'build script?'}
version=${3:?'version?'}

cd ${builddir}
git fetch --tags --prune --prune-tags
git checkout ${version}

if ! test -x "./${build_script}"; then
	echo "[ERROR] build script not found: ./${build_script} (build dir: ${build_dir})" >&2
	exit 9
fi

exec ./${build_script}
