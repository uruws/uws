FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.02"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh munin munin-node munin-plugins-extra

ADD ./utils /root/bin
RUN chmod -v 0750 /root/bin /root/bin/*.sh

ENTRYPOINT /root/bin/munin-start.sh
