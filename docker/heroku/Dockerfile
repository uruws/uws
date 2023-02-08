FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="230208"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

# https://github.com/heroku/cli/blob/master/install-standalone.sh
RUN cd /usr/local \
	&& wget -q -O heroku.tgz https://cli-assets.heroku.com/heroku-linux-x64.tar.gz \
	&& tar -xf heroku.tgz \
	&& rm -vf heroku.tgz \
	&& ln -svf /usr/local/heroku/bin/heroku /usr/local/bin/heroku

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN mkdir -vp ~/.cache/heroku
RUN heroku version \
	&& heroku plugins:install heroku-slugs

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

COPY --chown=uws:uws ./utils/*.sh /usr/local/bin/
RUN chmod -v 0555 /usr/local/bin/*.sh

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

CMD exec /usr/local/bin/uws-login.sh
