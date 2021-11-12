FROM uws/python-2109

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="211111"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN install -v -d -o uws -g uws -m 0750 /srv/home/uwscli \
	/srv/home/uwscli/bin /srv/home/uwscli/etc

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN mkdir -vp ~/tmp

RUN echo 'export PATH=/srv/home/uwscli/bin:${PATH}' >>~/.profile
