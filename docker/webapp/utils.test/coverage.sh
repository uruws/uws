#!/bin/sh
set -eu

webapp=${UWS_WEBAPP}
webapp_dir="/opt/uws/${webapp}"

PYTHONPATH=/opt/uws/lib:${webapp_dir}:/etc${webapp_dir}:${webapp_dir}/test
export PYTHONPATH

cd ${HOME}/tmp

rm -f .coverage

testfn=${1:-''}
if test -f "${webapp_dir}/${testfn}"; then
	shift
	/opt/uws/venv/bin/python3 -m coverage run ${webapp_dir}/${testfn} "$@"
else
	for t in ${webapp_dir}/test/*_test.py; do
		echo "*** ${t}"
		/opt/uws/venv/bin/python3 -m coverage run --append ${t} "$@"
	done
fi

covd=${HOME}/tmp/htmlcov
rm -rf ${covd}

/opt/uws/venv/bin/python3 -m coverage report --omit '/opt/uws/venv/*,/opt/uws/lib/*,/usr/lib/*'
/opt/uws/venv/bin/python3 -m coverage html --omit '/opt/uws/venv/*,/opt/uws/lib/*,/usr/lib/*' -d ${covd}

exit 0
