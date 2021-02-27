FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.02.27-1"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ARG UWSRUN_UID=1000
ARG UWSRUN_GID=1000

RUN groupadd -f -g ${UWSRUN_GID} uwsrun \
	&& useradd -o -d /home/uwsrun -m -c 'uwsrun' -g ${UWSRUN_GID} -u ${UWSRUN_UID} uwsrun \
	&& chmod -v 0750 /home/uwsrun \
	&& adduser uwsrun uws

RUN mkdir -vp /uws/var /uws/etc/env/bot \
	&& chown -vR uwsrun:uws /uws \
	&& chmod -vR 0750 /uws

COPY ./build/uwsbot.bin /usr/local/bin/uwsbot
RUN chmod -v 0755 /usr/local/bin/uwsbot

COPY --chown=uws:uws ./build/env.default /uws/etc/env/bot/default
RUN chmod -v 0640 /uws/etc/env/bot/default

USER uwsrun:uwsrun
WORKDIR /home/uwsrun

ENV USER uwsrun
ENV HOME /home/uwsrun

ENTRYPOINT ["uwsbot"]
