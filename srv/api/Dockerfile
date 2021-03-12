FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.03.11"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ADD ./utils /usr/local/bin
RUN chgrp -v uws /usr/local/bin/*.sh \
	&& chmod -v 0750 /usr/local/bin/*.sh

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

ENTRYPOINT exec /usr/local/bin/meteor-start.sh
