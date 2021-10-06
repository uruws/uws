FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="211006"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh python3 python3-doc

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /uws

WORKDIR /opt/uws
ENTRYPOINT /usr/local/bin/uws-login.sh
