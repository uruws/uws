#!/bin/sh
set -eu

UWS_WEBAPP_NQDIR=$(mktemp -d -p /tmp wappnq.XXXXXXXXXX)
export UWS_WEBAPP_NQDIR

PYTHONPATH=/opt/uws/lib:/opt/uws/lib/test
export PYTHONPATH

cd ${HOME}/tmp

rm -f .coverage

testfn=${1:-''}
if test -f "/opt/uws/lib/${testfn}"; then
	shift
	/opt/uws/venv/bin/python3 -m coverage run "/opt/uws/lib/${testfn}" "$@"
else
	for t in /opt/uws/lib/test/*_test.py; do
		echo "*** ${t}"
		/opt/uws/venv/bin/python3 -m coverage run --append "${t}" "$@"
	done
fi

covd=${HOME}/tmp/htmlcov
rm -rf ${covd}

/opt/uws/venv/bin/python3 -m coverage report --omit '/usr/lib/*'
/opt/uws/venv/bin/python3 -m coverage html   --omit '/usr/lib/*' -d ${covd}

exit 0
