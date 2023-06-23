#!/bin/sh
set -eu
CA=${PWD}/secret/ca/uws/smtps/230503
mkdir -vp ${PWD}/tmp
exec docker run -it --rm --name uws-mailx-devel \
	--hostname mailx-devel.uws.local \
	--read-only \
	-v ${PWD}/secret/eks/files/aws.ses:/etc/opt/uws:ro \
	-v ${PWD}/docker/mailx/utils:/usr/local/uws:ro \
	-v ${PWD}/tmp:/home/uws/tmp \
	-v ${CA}:/srv/etc/ca:ro \
	-u uws \
	-e USER=uws \
	-e HOME=/home/uws \
	--workdir /home/uws \
	--entrypoint /usr/local/bin/uws-login.sh \
	--tmpfs /tmp \
	uws/mailx-2305
