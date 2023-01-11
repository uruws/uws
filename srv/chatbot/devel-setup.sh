#!/bin/sh
set -eu

echo 'chatbotdev.uws.talkingpts.org' | sudo -n tee -a /uws/acme-certs.list
/uws/acme-certs.sh

sudo -n install -v -m 0644 ./srv/chatbot/etc/nginx-chatbot.conf /etc/nginx/sites-enabled/chatbotdev

sudo -n nginx -t
sudo -n service nginx reload

exit 0
