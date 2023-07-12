#!/bin/sh
set -eu

#echo "*** webapp/shellcheck.sh"
#/opt/uws/test/self/shellcheck.sh

echo "*** webapp/typecheck.sh"
/opt/uws/test/self/typecheck.sh

echo "*** webapp/coverage.sh"
/opt/uws/test/self/coverage.sh

exit 0
