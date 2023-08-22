#!/bin/sh
set -eu

ns=${TAPO_API_NAMESPACE}
replicas=${TAPO_API_REPLICAS}

for idx in $(seq 0 "${replicas}"); do
	echo '---'
	echo 'apiVersion: v1'
	echo 'kind: Service'
	echo 'metadata:'
	echo "  name: meteor${idx}-${ns}"
	echo 'spec:'
	echo '  type: ExternalName'
	echo "  externalName: meteor.${ns}.svc.cluster.local"
done

exit 0
