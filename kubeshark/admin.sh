#!/bin/sh
set -eu

uws_cluster=${1:?'cluster?'}
shift

awsdir=${PWD}/secret/eks/aws/client/${uws_cluster}
ksdir=${PWD}/kubeshark

tmpdir=${PWD}/tmp/kubeshark
mkdir -vp "${tmpdir}"

kubedir=${PWD}/secret/eks/kube/cluster/${uws_cluster}
mkdir -vp "${kubedir}"

eksenv=${PWD}/eks/env/${uws_cluster}.env

# shellcheck disable=SC1090
. ${eksenv}

hostname="${uws_cluster}.${AWS_REGION}.ksadm"
name="kubeshark-admin-${uws_cluster}"

echo 'http://localhost:8899/'

exec docker run -it --rm -u uws \
	--name "${name}" \
	--hostname "${hostname}" \
	-p 127.0.0.1:8898:8898 \
	-p 127.0.0.1:8899:8899 \
	-v "${awsdir}:/home/uws/.aws:ro" \
	-v "${kubedir}:/home/uws/.kube/eksctl/clusters:ro" \
	-v "${ksdir}:/home/uws/kubeshark:ro" \
	-v "${tmpdir}:/home/uws/tmp" \
	--env-file "${eksenv}" \
	"uws/${K8S_IMAGE}-2211"
