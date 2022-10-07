#!/bin/sh
set -eu

profile="${UWSCLI_PROFILE}"

adduser uws ssl-cert
adduser uws msmtp

echo "${profile}.cli.uws.talkingpts.org" >/etc/mailname
echo 'set mta=/usr/bin/msmtp'           >>/etc/mail.rc

install -v -m 0644 /srv/home/uwscli/etc/msmtprc /etc/msmtprc

#/etc/init.d/msmtpd start
exit 0
