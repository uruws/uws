FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.11"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh rsyslog cron munin

ENV MV 98aeca5f7b8e791360a962e625f5afcebdcce965
ENV MT munstrap
RUN wget -O munin-contrib.tgz \
	https://github.com/munin-monitoring/contrib/archive/${MV}.tar.gz \
	&& tar -xzf munin-contrib.tgz \
	&& rm -vf munin-contrib.tgz \
	&& mkdir -vp /uws/munin \
	&& mv -vf contrib-${MV} /uws/munin/contrib \
	&& rm -rvf /etc/munin/templates /etc/munin/static \
	&& cp -vr /uws/munin/contrib/templates/${MT}/templates /etc/munin \
	&& cp -vr /uws/munin/contrib/templates/${MT}/static /etc/munin \
	&& rm -rf /uws/munin/contrib

ADD ./utils /root/bin
RUN chmod -v 0750 /root/bin /root/bin/*.sh

COPY ./files/etc/rsyslog.conf /etc/
COPY ./files/etc/rsyslog.d/ /etc/rsyslog.d/
COPY --chown=root:munin ./files/etc/munin/ /etc/munin/

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

#~ CMD exec /bin/bash -l
ENTRYPOINT exec /root/bin/munin-start.sh
