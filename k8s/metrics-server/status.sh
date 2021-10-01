#!/bin/sh
set -eu
uwskube get pod,svc,deploy,rs -n kube-system |
	grep -E '(metrics|NAME)|(^$)'
exit 0
