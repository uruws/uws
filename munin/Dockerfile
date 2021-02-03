FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.03"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-distsetup.sh testing main
RUN /root/bin/apt-install.sh rsyslog cron munin munin-node

ADD ./utils /root/bin
RUN chmod -v 0750 /root/bin /root/bin/*.sh

COPY ./files/etc/rsyslog.conf /etc/
COPY ./files/etc/rsyslog.d/ /etc/rsyslog.d/
COPY --chown=root:munin ./files/etc/munin/ /etc/munin/

RUN echo 'EXTRA_OPTS="-L 5"' >>/etc/default/cron

VOLUME /var/lib/munin
VOLUME /var/cache/munin/www
VOLUME /var/log/munin

#~ RUN rm -vf /var/log/munin/*.log \
#~ 	&& ln -vsf /dev/stderr /var/log/munin/munin-node.log \
#~ 	&& ln -vsf /dev/stderr /var/log/munin/munin-update.log

#~ USER uws:uws
#~ WORKDIR /home/uws

#~ ENV USER uws
#~ ENV HOME /home/uws

#~ CMD exec /bin/bash -l

ENTRYPOINT exec /root/bin/munin-start.sh
