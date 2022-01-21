#!/bin/sh
set -eu

export PYTHONPATH=/uws/lib/plugins

cd ${HOME}/tmp

rm -f .coverage

testfn=${1:-''}
if test -f "${HOME}/${testfn}"; then
	shift
	python3-coverage run ${HOME}/${testfn} "$@"
else
	for t in ${HOME}/test/plugins/*_test.py; do
		echo "*** ${t}"
		python3-coverage run --append ${t} "$@"
	done
fi

covd=${HOME}/tmp/htmlcov
rm -rf ${covd}

python3-coverage report
python3-coverage html -d ${covd}

exit 0
