FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.03.11"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

#RUN /root/bin/apt-install.sh

#ADD ./utils /root/bin
#RUN chmod -v 0750 /root/bin /root/bin/*.sh

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

CMD exec /usr/local/bin/uws-login.sh
#ENTRYPOINT exec /root/bin/munin-start.sh
