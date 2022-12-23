#!/bin/sh
set -eu

tmpdir=${PWD}/tmp/chatbot
install -v -d -m 0750 "${tmpdir}"

exec docker run -it --rm --read-only \
	--name uws-chatbot-devel \
	--hostname chatbot-devel.uws.local \
	--entrypoint /usr/local/bin/uws-login.sh \
	-v "${tmpdir}:/home/uws/tmp" \
	--workdir /home/uws \
	uws/chatbot-2211
