#!/bin/sh
exec docker run -it --rm --name uws-mkcert-devel \
	--hostname mkcert-devel.uws.local \
	-v ${PWD}/docker/mkcert/utils:/home/uws/utils:ro \
	-v ${PWD}/docker/mkcert/etc:/usr/local/etc/ssl:ro \
	-v ${PWD}/secret/ca/uws/ops/etc:/usr/local/etc/ca:ro \
	-v ${PWD}/secret/ca/uws/ops/210820:/home/uws/ca \
	--workdir /home/uws/utils \
	-u uws uws/mkcert-2211 /bin/bash -l
