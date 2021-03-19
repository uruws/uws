FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.02.11"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh munin-node psmisc procps munin-plugins-core munin-plugins-extra \
	&& rm -vf /etc/munin/plugins/*

ENV MN munin-contrib
ENV MR uruws/${MN}
ENV MV 52861dd158e7a9b77b46dd718fae4ddea9cd0790
RUN wget -O munin-contrib.tgz \
	https://github.com/${MR}/archive/${MV}.tar.gz \
	&& tar -xzf munin-contrib.tgz \
	&& rm -vf munin-contrib.tgz \
	&& mkdir -vp /uws/munin \
	&& mv -vf ${MN}-${MV} /uws/munin/contrib

# mongodb plugins deps
RUN /root/bin/apt-install.sh python3-pymongo

ADD ./utils /root/bin
RUN chmod -v 0750 /root/bin /root/bin/*.sh

COPY --chown=uws:uws ./build/uwsbot-stats.bin /uws/bin/uwsbot-stats
RUN chmod -v 0750 /uws/bin/uwsbot-stats

COPY --chown=uws:uws ./build/uwsbot-stats.env /uws/etc/env/bot/stats
RUN chmod -v 0640 /uws/etc/env/bot/stats

COPY ./build/uwsbot-plugin.conf /etc/munin/plugin-conf.d/uwsbot
RUN chmod -v 0640 /etc/munin/plugin-conf.d/uwsbot

COPY --chown=uws:uws ./build/api-stats.bin /uws/bin/api-stats
RUN chmod -v 0750 /uws/bin/api-stats

ENTRYPOINT exec /root/bin/mn-start.sh
