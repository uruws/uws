FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="221116"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh clamav clamav-base clamav-freshclam
RUN freshclam

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

CMD exec /usr/local/bin/uws-login.sh
