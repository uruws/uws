FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="210819"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN (cd /usr/local/bin && \
	wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64) \
	&& chmod -v 0755 /usr/local/bin/mkcert-v1.4.3-linux-amd64 \
	&& ln -vsf /usr/local/bin/mkcert-v1.4.3-linux-amd64 /usr/local/bin/mkcert

RUN /root/bin/apt-install.sh uuid-runtime

ADD ./utils /usr/local/bin
RUN chmod -v 0755 /usr/local/bin/*.sh

VOLUME /home/uws/ca

USER uws:uws
WORKDIR /home/uws/ca

ENV USER uws
ENV HOME /home/uws
ENV CAROOT /home/uws/ca
ENV TRUST_STORES system

CMD exec mkcert
