#!/bin/sh
set -eu

echo '** ./eks/secrets/test/shellcheck.sh'
./eks/secrets/test/shellcheck.sh

echo '** ./eks/secrets/test/shellcheck-env-files.sh'
./eks/secrets/test/shellcheck-env-files.sh

exit 0
