#!/bin/sh
set -eu

echo "*** webapp: ${UWS_WEBAPP}"

exec uwsgi \
	--master \
	--no-orphans \
	--reload-on-exception \
	--vacuum \
	--enable-threads \
	--thunder-lock \
	--need-plugin           python3 \
	--max-apps              1 \
	--reload-mercy          30 \
	--worker-reload-mercy   10 \
	--max-requests          5000 \
	--min-worker-lifetime   180 \
	--max-worker-lifetime   28800 \
	--evil-reload-on-rss    1024 \
	--module                "${UWS_WEBAPP}_wsgi:application" \
	--env                   LANG=en_US.UTF-8 \
	--env                   LANGUAGE=en_US.UTF-8 \
	--env                   LC_ALL=en_US.UTF-8 \
	--env                   LC_CTYPE=UTF-8 \
	--env                   PYTHONUTF8=1 \
	--env                   PYTHONIOENCODING=utf-8 \
	--workers               "${UWS_WEBAPP_WORKERS}" \
	--http11-socket         "0.0.0.0:${UWS_WEBAPP_PORT}" \
	--chdir                 "/opt/uws/${UWS_WEBAPP}" \
	--venv                  /opt/uws/venv
