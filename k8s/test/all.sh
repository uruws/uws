#!/bin/sh
set -eu

echo '***** k8s/test/run/shellcheck.sh'
./k8s/test/run/shellcheck.sh

echo '***** k8s/test/run/typecheck.sh'
./k8s/test/run/typecheck.sh

echo '***** k8s/test/run/coverage.sh'
./k8s/test/run/coverage.sh

exit 0
