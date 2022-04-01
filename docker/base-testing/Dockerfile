FROM uws/base-2203

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220401"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-distsetup.sh bookworm main

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

CMD exec /bin/bash -l
