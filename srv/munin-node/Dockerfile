FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.11"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh munin-node psmisc procps munin-plugins-core munin-plugins-extra \
	&& rm -vf /etc/munin/plugins/*

ENV MV=0d13497ed83dd5927b77aad70e982ba16005a633
RUN wget -O munin-contrib.tgz \
	https://github.com/munin-monitoring/contrib/archive/${MV}.tar.gz \
	&& tar -xzf munin-contrib.tgz \
	&& rm -vf munin-contrib.tgz \
	&& mkdir -vp /uws/munin \
	&& mv -vf contrib-${MV} /uws/munin/contrib

ADD ./utils /root/bin
RUN chmod -v 0750 /root/bin /root/bin/*.sh

#~ VOLUME /var/lib/munin
#~ VOLUME /var/cache/munin/www
#~ VOLUME /var/log/munin

#~ CMD exec /bin/bash -l
ENTRYPOINT exec /root/bin/mn-start.sh
