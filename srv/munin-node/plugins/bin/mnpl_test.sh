#!/bin/sh
set -eu

action=${1:-"NONE"}

if test "X${action}" = 'Xconfig'; then
	echo 'graph_title munin-node plugin test'
	echo 'graph_args --base 1000 -l 0'
	echo 'graph_scale no'
	echo 'graph_vlabel value'
	echo 'graph_category uwstest'
	echo 'mnpl_test.label mnpl_test'
	echo 'mnpl_test.draw AREA'
	echo 'mnpl_test.min 0'
	echo 'mnpl_test.max 3'
	echo 'mnpl_test.warning 1'
	echo 'mnpl_test.critical 2'
	exit 0
fi

echo 'mnpl_test.value 0'
exit 0
