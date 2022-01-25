#!/bin/sh
set -eu
echo '***** munin-node/test/run/shellcheck.sh'
./test/run/shellcheck.sh

echo '***** munin-node/test/run/typecheck.sh'
./test/run/typecheck.sh

echo '***** munin-node/test/run/coverage.sh'
./test/run/coverage.sh

exit 0
