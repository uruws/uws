#!/bin/sh
set -eu

# Save current namespace/app version to be used as rollback.
# If there's no current version, just use the new one.

ns=${1:?'namespace?'}
new_version=${2:?'app version?'}

cur_version=$(./pod/lib/rollback-getcur.sh)
if test 'X' = "X${cur_version}"; then
	cur_version="${new_version}"
fi

uwskube delete configmap pod-deploy-rollback -n "${ns}" || true

envf=$(mktemp -p /tmp "pod-${ns}-deploy-rollback.XXXXXXXX")

echo "export AWS_REGION='${AWS_REGION}'" >${envf}
echo "export APP_VERSION='${cur_version}'" >>${envf}

echo "*** set rollback config:"
cat "${envf}"

uwskube create configmap pod-deploy-rollback -n "${ns}" --from-file="deploy-rollback=${envf}"
rm -f ${envf}

exit 0
