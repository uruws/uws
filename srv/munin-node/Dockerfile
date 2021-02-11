FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.11"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh munin-node psmisc procps munin-plugins-core munin-plugins-extra

#~ ADD ./utils /root/bin
#~ RUN chmod -v 0750 /root/bin /root/bin/*.sh

#~ COPY ./files/etc/rsyslog.conf /etc/
#~ COPY ./files/etc/rsyslog.d/ /etc/rsyslog.d/
#~ COPY --chown=root:munin ./files/etc/munin/ /etc/munin/

#~ RUN echo 'EXTRA_OPTS="-L 5"' >>/etc/default/cron

#~ VOLUME /var/lib/munin
#~ VOLUME /var/cache/munin/www
#~ VOLUME /var/log/munin

CMD exec /bin/bash -l
#~ ENTRYPOINT exec /root/bin/munin-start.sh
