#!/bin/sh
set -eu

sudo -n install -v -m 0640 -o uws -g uws \
	/srv/uws/deploy/host/assets/jsbatch/uws/acme-certs.list \
	/uws/acme-certs.list

sudo -n rm -vf /etc/nginx/sites-enabled/chatbotdev

sudo -n nginx -t
sudo -n service nginx reload

exit 0
