#!/bin/sh
set -eu

export PYTHONPATH=${HOME}/lib:${HOME}/test

covrc=/tmp/coveragerc

cd ${HOME}
rm -vf ${covrc}
touch ${covrc}
for t in $(ls test/*_test.py); do
	echo "*** ${t}"
	python3-coverage run --append --rcfile=${covrc} ${t} $@
done
covd=~/tmp/htmlcov
rm -rf ${covd}
python3-coverage html -d ${covd} --rcfile=${covrc}
exit 0
