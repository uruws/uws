#!/bin/sh
set -u
for j in $(uwskube get pods -n ctl | grep -F 'Error' | cut -d ' ' -f 1); do
	uwskube delete pod ${j} -n ctl
done
exit 0
