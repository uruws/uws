#!/bin/sh
set -eu

export PYTHONPATH=/srv/home/uwscli/lib:${HOME}/test

cd ${HOME}

rm -f .coverage

testfn=${1:-''}
if test "X${testfn}" != 'X'; then
	shift
	python3-coverage run ${testfn} $@
else
	for t in $(ls test/*_test.py); do
		echo "*** ${t}"
		python3-coverage run --append ${t} $@
	done
fi

covd=${HOME}/tmp/htmlcov
rm -rf ${covd}

python3-coverage report
python3-coverage html -d ${covd}

exit 0
