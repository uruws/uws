#!/bin/sh
ns=${1:?'namespace?'}
app=${2:?'app name?'}

uwskube get all -n "${ns}" -l "app.kubernetes.io/name=meteor-${app}"

echo
uwskube get "deployment/meteor-${app}" -n "${ns}"

appver=$(~/pod/tapo/deploy-getver.sh "${ns}" "${app}")

echo
echo 'DEPLOY'
echo -e "version\t${appver}"

exit 0
