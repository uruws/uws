#!/bin/sh
set -eu
uwskube get pod,deploy,rs -n kube-system |
	grep -E '(autoscaler|NAME)|(^$)'
exit 0
