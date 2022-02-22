FROM uws/base-2109

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220222"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh ssl-cert msmtp-mta bsd-mailx

RUN adduser uws ssl-cert

RUN install -v -d -o root -g root -m 0750 /srv/etc \
	&& install -v -d -o root -g root -m 0750 /srv/etc/ca \
	&& install -v -d -o root -g root -m 0750 /etc/opt/uws \
	&& install -v -d -o root -g root -m 0750 /etc/opt/uws/ca

RUN echo 'mailx.uws.talkingpts.org' >/etc/mailname

COPY ./files/etc/aliases /etc/
RUN chmod -v 0644 /etc/aliases

COPY ./files/etc/msmtprc /etc/
RUN chmod -v 0644 /etc/msmtprc

RUN echo 'set mta=/usr/bin/msmtp' >>/etc/mail.rc
