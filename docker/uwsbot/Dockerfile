FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.03.03"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN mkdir -vp /uws/var /uws/etc/env \
	&& chown -vR uws:uws /uws \
	&& chmod -vR 0750 /uws

COPY ./build/uwsbot.bin /usr/local/bin/uwsbot
COPY ./build/uwsbot-stats.bin /usr/local/bin/uwsbot-stats
RUN chmod -v 0755 /usr/local/bin/uwsbot*

COPY --chown=uws:uws ./build/env/bot /uws/etc/env/
RUN chmod -v 0640 /uws/etc/env/bot/*

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

ENTRYPOINT ["uwsbot"]
