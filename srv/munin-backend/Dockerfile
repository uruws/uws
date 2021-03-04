FROM uws/munin

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.03.04"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh apache2 ssl-cert libapache2-mod-fcgid

VOLUME /var/cache/munin/www

ADD ./utils /root/bin
RUN chmod -v 0750 /root/bin /root/bin/*.sh

COPY ./files/etc/apache2 /etc/apache2
COPY --chown=root:www-data ./files/var/www/html /var/www/html

ENTRYPOINT exec /root/bin/munin-backend-start.sh
