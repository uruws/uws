FROM uws/pod:base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="230515"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ADD ./build/podtest /usr/local/bin
RUN chgrp -v uws /usr/local/bin/podtest \
	&& chmod -v 0750 /usr/local/bin/podtest

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

EXPOSE 8699

ENTRYPOINT exec /usr/local/bin/podtest
