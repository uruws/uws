#!/bin/sh
set -eu
cd ${HOME}
export PYTHONPATH=${HOME}/bin
for t in $(ls cli/test/*_test.py); do
	echo "*** ${t}"
	python3 ${t} $@
done
exit 0
