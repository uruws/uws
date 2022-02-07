#!/bin/sh
set -eu

echo '***** cli/test/run/shellcheck.sh'
./test/run/shellcheck.sh

echo '***** cli/test/run/vendor.sh'
./test/run/vendor.sh

echo '***** cli/test/run/typecheck.sh'
./test/run/typecheck.sh

echo '***** cli/test/run/coverage.sh'
./test/run/coverage.sh

exit 0
