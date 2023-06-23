#!/bin/sh
set -eu
install -v -d -m 0750 "${PWD}/tmp/mailx"
awsses=${PWD}/secret/eks/files/mailx/aws.ses
chmod -v 0600 "${awsses}/msmtprc"
exec docker run -it --rm --name uws-mailx-devel \
	--hostname mailx-devel.uws.local \
	--read-only \
	-v "${awsses}:/etc/opt/mailx/uws:ro" \
	-v "${PWD}/tmp/mailx:/home/uws/tmp" \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	--workdir /home/uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	--tmpfs /tmp \
	--tmpfs /etc/opt/mailx \
	uws/mailx-2305
