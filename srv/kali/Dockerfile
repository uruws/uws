FROM kalilinux/kali-rolling

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="${UWS_VERSION}"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ADD ./utils/apt-*.sh /root/bin/
RUN chmod -v 0750 /root/bin /root/bin/*.sh

RUN /root/bin/apt-distupgrade.sh
RUN /root/bin/apt-install.sh bash ca-certificates wget locales less vim

RUN echo 'en_US.UTF-8 UTF-8' >/etc/locale.gen \
	&& locale-gen \
	&& update-locale LANG=en_US.UTF-8

ARG UWS_UID=1000
ARG UWS_GID=1000

RUN groupadd -o -g ${UWS_GID} uws \
	&& useradd -o -d /home/uws -m -c 'uws' -g ${UWS_GID} -u ${UWS_UID} uws \
	&& chmod -v 0750 /home/uws

RUN /root/bin/apt-install.sh kali-desktop-xfce

RUN /root/bin/apt-install.sh bzip2 xz-utils net-tools xrdp xorgxrdp xorg xbitmaps dbus-x11

RUN rm -vf /root/.bashrc \
	&& mv -v /root/.bashrc.original /root/.bashrc

ADD ./utils/kali-*.sh /usr/local/bin
RUN chmod -v 0755 /usr/local/bin/kali-*.sh

CMD exec /bin/bash -l
