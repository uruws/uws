#!/bin/sh
set -eu

if test 'X' = "${UWS_WEBAPP_NQDIR:-X}"; then
	UWS_WEBAPP_NQDIR=$(mktemp -d -p /tmp wappnq.XXXXXXXXXX)
	export UWS_WEBAPP_NQDIR
fi

echo "*** webapp: ${UWS_WEBAPP}"
echo "***   port: ${UWS_WEBAPP_PORT}"
echo "***     nq: ${UWS_WEBAPP_NQDIR}"

if test -s "/opt/uws/${UWS_WEBAPP}/VERSION"; then
	echo "${UWS_WEBAPP} version $(cat "/opt/uws/${UWS_WEBAPP}/VERSION")"
fi

pypath=/opt/uws/lib:/etc/opt/uws/${UWS_WEBAPP}

exec uwsgi                                                        \
	--master                                                      \
	--no-orphans                                                  \
	--die-on-term                                                 \
	--exit-on-reload                                              \
	--reload-on-exception                                         \
	--vacuum                                                      \
	--enable-threads                                              \
	--thunder-lock                                                \
	--need-plugin         python3                                 \
	--max-apps            1                                       \
	--worker-reload-mercy 5                                       \
	--min-worker-lifetime 3                                       \
	--workers             "${UWS_WEBAPP_WORKERS}"                 \
	--module              "${UWS_WEBAPP}_wsgi:application"        \
	--env                 LANG=en_US.UTF-8                        \
	--env                 LANGUAGE=en_US.UTF-8                    \
	--env                 LC_ALL=en_US.UTF-8                      \
	--env                 LC_CTYPE=UTF-8                          \
	--env                 PYTHONUTF8=1                            \
	--env                 PYTHONIOENCODING=utf-8                  \
	--env                 "PYTHONPATH=${pypath}"                  \
	--http11-socket       "0.0.0.0:${UWS_WEBAPP_PORT}"            \
	--chdir               "/opt/uws/${UWS_WEBAPP}"                \
	--venv                /opt/uws/venv
