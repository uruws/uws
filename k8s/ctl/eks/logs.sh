#!/bin/sh
set -eu
for j in $(uwskube get jobs -n ctl -o name); do
	uwskube logs ${j} -n ctl $@
done
exit 0
