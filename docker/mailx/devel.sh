#!/bin/sh
set -eu
install -v -d -m 0750 ${PWD}/tmp/mailx
chmod -v 0600 ${PWD}/secret/eks/files/aws.ses/msmtprc
exec docker run -it --rm --name uws-mailx-devel \
	--hostname mailx-devel.uws.local \
	--read-only \
	-v ${PWD}/secret/eks/files/aws.ses:/etc/opt/uws:ro \
	-v ${PWD}/docker/mailx/utils:/usr/local/uws:ro \
	-v ${PWD}/tmp/mailx:/home/uws/tmp \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	--workdir /home/uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	--tmpfs /tmp \
	uws/mailx-2305
