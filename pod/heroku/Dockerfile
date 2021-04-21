FROM uwspod/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="20210420"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ADD ./utils /usr/local/bin
RUN chgrp -v uws /usr/local/bin/*.sh \
	&& chmod -v 0750 /usr/local/bin/*.sh

RUN install -v -d -m 0750 -o uws -g uws /home/uws/meteor/app

ARG APP=heroku_app_not_set
ADD --chown=uws:uws ./download/${APP}/app /home/uws/meteor/app

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

EXPOSE 3000

ENTRYPOINT exec /usr/local/bin/meteor-start.sh
