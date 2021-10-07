FROM uws/base-2109

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="211006"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh rsyslog cron logrotate munin python3

ENV MN munin-contrib
ENV MR uruws/${MN}
ENV MV 22ba05175f518b67525883bd1864c90a68eb2e1e
ENV MT munstrap
RUN wget -O munin-contrib.tgz \
	https://github.com/${MR}/archive/${MV}.tar.gz \
	&& tar -xzf munin-contrib.tgz \
	&& rm -vf munin-contrib.tgz \
	&& mkdir -vp /uws/munin \
	&& mv -vf ${MN}-${MV} /uws/munin/contrib \
	&& rm -rvf /etc/munin/templates /etc/munin/static \
	&& cp -vr /uws/munin/contrib/templates/${MT}/templates /etc/munin \
	&& cp -vr /uws/munin/contrib/templates/${MT}/static /etc/munin \
	&& rm -rf /uws/munin/contrib

COPY --chown=root:munin ./files/etc/munin/templates.patch /etc/munin/
COPY --chown=root:munin ./files/etc/munin/static/ /etc/munin/static/

RUN /root/bin/apt-install.sh patch \
	&& cd /etc/munin \
	&& patch -p0 <templates.patch \
	&& /root/bin/apt-autoremove.sh patch \
	&& chmod -v 0755 /etc/munin/static /etc/munin/static/css \
	&& chmod -v 0644 /etc/munin/static/css/uws.css

RUN echo 'EXTRA_OPTS="-L 5"' >>/etc/default/cron

VOLUME /var/lib/munin
VOLUME /var/cache/munin/www
VOLUME /var/log/munin

RUN /root/bin/apt-install.sh ssl-cert

RUN adduser uws munin \
	&& adduser uws ssl-cert

COPY ./files/etc/cron.d/uws /etc/cron.d/uws

COPY ./files/etc/rsyslog.conf /etc/
COPY ./files/etc/rsyslog.d/ /etc/rsyslog.d/

COPY --chown=root:munin ./files/etc/munin/munin.conf /etc/munin/

RUN install -v -d -m 0755 /opt/munin/lib

COPY ./utils/bin /usr/local/bin
RUN chmod -v 0755 /usr/local/bin/munin-*.*

COPY ./utils/lib /opt/munin/lib
RUN chmod -v 0644 /opt/munin/lib/*.*
RUN python3 -m compileall /opt/munin/lib

ENTRYPOINT exec /usr/local/bin/munin-start.sh
