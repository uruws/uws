FROM uws/base-2109

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="211011"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh python3 ansible python3-libcloud ansible-lint

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN mkdir -vp -m 0750 /home/uws/.ansible

RUN ansible --version \
	&& rm -rf /home/uws/.ansible/tmp

ENTRYPOINT /usr/local/bin/uws-login.sh
