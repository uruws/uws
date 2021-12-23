#!/bin/sh
set -eu
export PYTHONPATH=${HOME}/utils/lib:${HOME}/utils/test

script=${1}
shift

cd ${HOME}/tmp
rm -f .coverage

python3-coverage run ${HOME}/${script} "$@"

covd=${HOME}/tmp/htmlcov
rm -rf ${covd}

python3-coverage report
python3-coverage html -d ${covd}

exit 0
