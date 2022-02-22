FROM uws/base-2109

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220222"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh rsyslog cron logrotate ssl-cert

RUN adduser uws ssl-cert

COPY ./files/etc/rsyslog.conf /etc/
COPY ./files/etc/rsyslog.d/ /etc/rsyslog.d/

RUN echo 'EXTRA_OPTS="-L 5"' >>/etc/default/cron

###COPY ./files/etc/cron.d/uws /etc/cron.d/uws

RUN install -v -d -o root -g root -m 0750 /srv/etc \
	&& install -v -d -o root -g root -m 0750 /srv/etc/ca

COPY ./utils /usr/local/bin
RUN chmod -v 0755 /usr/local/bin/*.sh

ENTRYPOINT exec /usr/local/bin/entrypoint.sh
