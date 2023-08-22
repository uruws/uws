#!/bin/sh
set -eu

ns=${TAPO_API_NAMESPACE}
replicas=${TAPO_API_REPLICAS}

echo "upstream meteor-${ns} {"
echo '    random two least_conn;'
for idx in $(seq 0 "${replicas}"); do
	echo "    server meteor${idx}-${ns}:3000;"
done
echo '}'

exit 0
