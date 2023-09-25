#!/bin/sh
set -eu

CHATBOT_TAG=$(cat ./srv/chatbot/VERSION)

./host/ecr-login.sh   us-east-1
./cluster/ecr-push.sh us-east-1 uws/chatbot-2309 "uws:chatbot-${CHATBOT_TAG}"

if test -d /srv/www/ssl/htmlcov; then
	if test -d ./tmp/chatbot/htmlcov; then
		umask 0022
		cp -r ./tmp/chatbot/htmlcov /srv/www/ssl/htmlcov/chatbot
		echo '/srv/www/ssl/htmlcov/chatbot done!'
	fi
fi

exit 0
