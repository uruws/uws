#!/bin/sh
set -eu

rm -f .coverage

testfn=${1:-''}
if test "X${testfn}" != 'X'; then
	shift
	python3-coverage run ${testfn} "$@"
else
	find k8s/test/ -type f -name '*_test.py' | sort | while read t
	do
		echo "*** ${t}"
		python3-coverage run --append ${t} "$@"
	done
fi

covd=${HOME}/tmp/htmlcov
rm -rf ${covd}

python3-coverage report --omit '/uws/lib/plugins/*.py'
python3-coverage html   --omit '/uws/lib/plugins/*.py' -d ${covd}

exit 0
