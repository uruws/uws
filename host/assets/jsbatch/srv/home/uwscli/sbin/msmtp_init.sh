#!/bin/sh
set -eu

profile="${UWSCLI_PROFILE}"

adduser uws    ssl-cert
adduser uws    msmtp
adduser uwscli msmtp

echo "${profile}.cli.uws.talkingpts.org" >/etc/mailname
echo 'set mta=/usr/bin/msmtp'           >>/etc/mail.rc

install -v -m 0644 /srv/home/uwscli/etc/aliases /etc/aliases

#~ export UWSCLI_PROFILE
tmpfn=$(mktemp /tmp/msmtp_init.XXXXXXXXXXXXXXXX)
envsubst </srv/home/uwscli/etc/msmtprc.in >${tmpfn}
install -v -m 0644 "${tmpfn}" /etc/msmtprc
rm -f "${tmpfn}"

install -v -d -o root -g msmtp -m 0750 /usr/local/ca/smtps
install -v -d -o root -g msmtp -m 0750 /usr/local/ca/smtps/client

install -v -o root -g msmtp -m 0640 /srv/etc/ca/smtps/rootCA.pem \
	/usr/local/ca/smtps/
install -v -o root -g msmtp -m 0640 /srv/etc/ca/smtps/rootCA-crl.pem \
	/usr/local/ca/smtps/

install -v -o root -g msmtp -m 0640 \
	/srv/etc/ca/smtps/client/08082dca-8d77-5c81-9a44-94642089b3b1.pem \
	/usr/local/ca/smtps/client/
install -v -o root -g msmtp -m 0640 \
	/srv/etc/ca/smtps/client/08082dca-8d77-5c81-9a44-94642089b3b1.key \
	/usr/local/ca/smtps/client/

#/etc/init.d/msmtpd start
exit 0
