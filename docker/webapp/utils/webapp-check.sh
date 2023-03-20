#!/bin/sh
set -eu

webapp=${UWS_WEBAPP}
cd "/opt/uws/${webapp}"

echo "*** ${webapp}/test/run/shellcheck.sh"
./test/run/shellcheck.sh

echo "*** ${webapp}/test/run/typecheck.sh"
./test/run/typecheck.sh

echo "*** ${webapp}/test/run/coverage.sh"
./test/run/coverage.sh

exit 0
