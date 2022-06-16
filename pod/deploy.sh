#!/bin/sh
set -eu

lastimg() {
	~/pod/lastimg.py "${1}"
}

if test "X${APP_REPLICAS:-X}" != 'XX'; then
	ver=$(lastimg meteor-app)
	echo "*** pod/meteor/web/deploy.sh ${ver}"
	~/pod/meteor/web/deploy.sh "$(lastimg meteor-app)"
fi

if test "X${METEOR_WORKER_REPLICAS:-X}" != 'XX'; then
	ver=$(lastimg meteor-app)
	echo "*** pod/meteor/worker/deploy.sh ${ver}"
	~/pod/meteor/worker/deploy.sh "${ver}"
fi

if test "X${METEOR_CS_REPLICAS:-X}" != 'XX'; then
	ver=$(lastimg meteor-crowdsourcing)
	echo "*** pod/meteor/cs/deploy.sh ${ver}"
	~/pod/meteor/cs/deploy.sh "${ver}"
fi

if test "X${INFRA_UI_REPLICAS:-X}" != 'XX'; then
	ver=$(lastimg meteor-infra-ui)
	echo "*** pod/meteor/infra-ui/deploy.sh ${ver}"
	~/pod/meteor/infra-ui/deploy.sh "${ver}"
fi

exit 0
