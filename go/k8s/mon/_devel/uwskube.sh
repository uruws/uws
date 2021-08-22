#!/bin/sh
set -eu
datadir=/go/tmp/k8smon/${UWS_CLUSTER}

fn=${datadir}/NOT_FOUND
if test 'Xget nodes -o json' = "X$*"; then
	fn=nodes.json
fi
datfn=${datadir}/${fn}

exec cat ${datfn}
