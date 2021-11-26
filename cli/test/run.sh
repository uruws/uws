#!/bin/sh
set -eu
cd ${HOME}
for t in test/*_test.py; do
	echo "*** ${t}"
	python3 ${t} "$@"
done
exit 0
