#!/bin/sh
set -eu
./test/run/shellcheck.sh
./test/run/typecheck.sh
./test/run/coverage.sh
exit 0
