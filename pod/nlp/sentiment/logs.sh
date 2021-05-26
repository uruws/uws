#!/bin/sh
set -eu
if test -n ${1:-''}; then
	if test 'X-f' != "X${1}"; then
		uwskube logs -n nlp --tail=10 --timestamps $@
		exit 0
	fi
fi
uwskube logs -n nlp --tail=1 --max-log-requests=100 --prefix=true --timestamps --ignore-errors -l 'app.kubernetes.io/name=nlp-sentiment' $@
exit 0
