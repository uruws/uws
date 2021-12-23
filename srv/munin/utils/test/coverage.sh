#!/bin/sh
set -eu

export PYTHONPATH=${HOME}/utils/lib:${HOME}/utils/test

cd ${HOME}/tmp

rm -f .coverage

for t in ${HOME}/utils/test/*_test.py; do
	echo "*** ${t}"
	python3-coverage run --append ${t} -v
done

covd=${HOME}/tmp/htmlcov
rm -rf ${covd}

python3-coverage report
python3-coverage html -d ${covd}

exit 0
