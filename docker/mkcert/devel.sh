#!/bin/sh
exec docker run -it --rm --name uws-mkcert-devel \
	--hostname mkcert-devel.uws.local \
	-v ${PWD}/docker/mkcert/utils:/home/uws/utils \
	-v ${PWD}/secret/ca/uws:/home/uws/ca \
	--workdir /home/uws/utils \
	-u uws uws/mkcert /bin/bash -l
