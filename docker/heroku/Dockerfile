FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.03.10"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh nodejs

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

CMD exec /usr/local/bin/uws-login.sh
