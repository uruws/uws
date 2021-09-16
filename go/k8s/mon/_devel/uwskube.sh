#!/bin/sh
set -eu
datadir=/go/tmp/k8smon/${UWS_CLUSTER}

fn=${datadir}/NOTSET_IN_DEVEL_UWSKUBE_SH
if test 'Xget nodes -o json' = "X$*"; then
	fn=nodes.json
elif test 'Xget deployments,statefulset,daemonset -A -o json' = "X$*"; then
	fn=deployments.json
elif test 'Xget pods -A -o json' = "X$*"; then
	fn=pods.json
fi
datfn=${datadir}/${fn}

exec cat ${datfn}
