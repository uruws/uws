FROM uws/base-2109

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="211110"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh less python3 python3-coverage

RUN groupadd -o -g 1700 uwscli \
	&& useradd -o -d /srv/home/uwscli -m -c 'uwscli' -g 1700 -u 1700 uwscli \
	&& chmod -v 0750 /srv/home/uwscli \
	&& adduser uwscli uws

USER uwscli:uwscli
WORKDIR /srv/home/uwscli

ENV USER uwscli
ENV HOME /srv/home/uwscli

RUN mkdir -vp -m 0750 ~/bin ~/etc

CMD exec /bin/bash -il
