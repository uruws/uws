#!/bin/sh
set -eu

if test "X${APP_REPLICAS:-X}" != 'XX'; then
	echo '*** pod/meteor/web/teardown.sh'
	~/pod/meteor/web/teardown.sh
fi

if test "X${METEOR_WORKER_REPLICAS:-X}" != 'XX'; then
	echo '*** pod/meteor/worker/teardown.sh'
	~/pod/meteor/worker/teardown.sh
fi

if test "X${METEOR_CS_REPLICAS:-X}" != 'XX'; then
	echo '*** pod/meteor/cs/teardown.sh'
	~/pod/meteor/cs/teardown.sh
fi

if test "X${INFRA_UI_REPLICAS:-X}" != 'XX'; then
	echo '*** pod/meteor/infra-ui/teardown.sh'
	~/pod/meteor/infra-ui/teardown.sh
fi

exit 0
