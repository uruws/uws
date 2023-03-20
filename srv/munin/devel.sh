#!/bin/sh
set -eu
CA=${PWD}/secret/ca/uws/smtps/211006
mkdir -vp ${PWD}/tmp
exec docker run -it --rm --name uws-munin-devel \
	--hostname munin-devel.uws.local \
	--read-only \
	-u uws --entrypoint /usr/local/bin/uws-login.sh \
	-e USER=uws -e HOME=/home/uws \
	-e UWS_SMTPS_CERT='/etc/opt/uws/ca/client/08082dca-8d77-5c81-9a44-94642089b3b1.pem' \
	-e UWS_SMTPS_KEY='/etc/opt/uws/ca/client/08082dca-8d77-5c81-9a44-94642089b3b1.key' \
	-v ${PWD}/srv/munin/utils:/opt/munin \
	-v ${PWD}/tmp:/home/uws/tmp \
	-v ${PWD}/python:/opt/uws \
	-v ${CA}:/etc/opt/uws/ca:ro \
	--tmpfs /var/opt/munin-alert \
	--workdir /opt/munin \
	$@ uws/munin-2211
