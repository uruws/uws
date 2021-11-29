#!/bin/bash
set -eu
pushd /srv/home/uwscli/vendor

pushd semver-2.13.0
pytest-3
popd

popd
exit 0
