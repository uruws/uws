#!/bin/sh
set -eu
export PYTHONPATH=${HOME}/lib:${HOME}/test
cd ${HOME}
for t in $(ls test/*_test.py); do
	echo "*** ${t}"
	python3-coverage run ${t} $@
done
python3-coverage html
exit 0
