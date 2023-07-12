#!/bin/sh
set -eu

webapp=${UWS_WEBAPP}
cd "/opt/uws/${webapp}"

echo "*** shellcheck.sh"
/opt/uws/test/shellcheck.sh

echo "*** typecheck.sh"
/opt/uws/test/typecheck.sh

echo "*** coverage.sh"
/opt/uws/test/coverage.sh

exit 0
