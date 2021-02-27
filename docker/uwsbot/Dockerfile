FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.02.27"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN mkdir -vp /uws \
	&& chown -vR uws:uws /uws \
	&& chmod -vR 0750 /uws

COPY ./build/uwsbot.bin /usr/local/bin/uwsbot
RUN chmod -v 0755 /usr/local/bin/uwsbot

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

ENTRYPOINT exec /usr/local/bin/uwsbot
