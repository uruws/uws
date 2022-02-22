FROM uws/mailx

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220222"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh rsyslog cron logrotate

COPY ./files/etc/rsyslog.conf /etc/
COPY ./files/etc/rsyslog.d/ /etc/rsyslog.d/

RUN echo 'EXTRA_OPTS="-L 5"' >>/etc/default/cron

###COPY ./files/etc/cron.d/uws /etc/cron.d/uws

COPY ./utils /usr/local/bin
RUN chmod -v 0755 /usr/local/bin/*.sh

ENTRYPOINT exec /usr/local/bin/entrypoint.sh
