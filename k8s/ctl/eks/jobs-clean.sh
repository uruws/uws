#!/bin/sh
set -u
for j in $(uwskube get pods -n ctl -o name); do
	uwskube delete ${j} -n ctl
done
for j in $(uwskube get jobs -n ctl -o name); do
	uwskube delete ${j} -n ctl
done
exit 0
