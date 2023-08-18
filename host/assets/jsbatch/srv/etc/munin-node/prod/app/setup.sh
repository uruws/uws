#!/bin/sh
set -eu

pl_ena=/root/bin/plugin-enable.sh

${pl_ena} http_loadtime http_loadtime

${pl_ena} contrib mongodb/mongodb_conn mongodb_conn
${pl_ena} contrib mongodb/mongodb_docs mongodb_docs
${pl_ena} contrib mongodb/mongo_lag mongo_lag
${pl_ena} contrib mongodb/mongo_mem mongo_mem
${pl_ena} contrib mongodb/mongo_ops mongo_ops

${pl_ena} contrib ssl/ssl-certificate-expiry ssl-certificate-expiry

rm -vf /etc/munin/plugins/uwsbot_stats
ln -svf /uws/bin/uwsbot-stats /etc/munin/plugins/uwsbot_stats

rm -vf /etc/munin/plugins/api*
ln -svf /uws/bin/api-job-stats /etc/munin/plugins/api_job_stats

rm -vf /etc/munin/plugins/uws_*
ln -svf /uws/bin/offlinepage.sh /etc/munin/plugins/uws_offlinepage_app

exit 0
