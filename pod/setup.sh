#!/bin/sh
set -eu

if test "X${APP_REPLICAS:-X}" != 'XX'; then
	echo '*** pod/meteor/web/setup.sh'
	~/pod/meteor/web/setup.sh
fi

if test "X${METEOR_WORKER_REPLICAS:-X}" != 'XX'; then
	echo '*** pod/meteor/worker/setup.sh'
	~/pod/meteor/worker/setup.sh
fi

if test "X${METEOR_CS_REPLICAS:-X}" != 'XX'; then
	echo '*** pod/meteor/cs/setup.sh'
	~/pod/meteor/cs/setup.sh
fi

if test "X${INFRA_UI_REPLICAS:-X}" != 'XX'; then
	echo '*** pod/meteor/infra-ui/setup.sh'
	~/pod/meteor/infra-ui/setup.sh
fi

exit 0
