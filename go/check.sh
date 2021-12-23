#!/bin/sh
set -eu
cd /go/src/uws

echo '*** ./_test/shellcheck.sh'
./_test/shellcheck.sh

exit 0
