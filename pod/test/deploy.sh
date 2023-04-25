#!/bin/sh
set -eu
version=$(cat ${HOME}/pod/test/VERSION)
exec ~/pod/lib/deploy.sh default test "${version}"
