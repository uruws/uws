#!/bin/bash
set -eu

rm -rf ${HOME}/tmp/htmlcov_vendor
mkdir -vp ${HOME}/tmp/htmlcov_vendor

pushd /srv/home/uwscli/vendor

pushd semver-2.13.0
pytest-3 --color=auto --cov-report=html:${HOME}/tmp/htmlcov_vendor
popd

popd
exit 0
