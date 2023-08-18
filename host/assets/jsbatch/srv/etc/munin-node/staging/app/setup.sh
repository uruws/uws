#!/bin/sh
set -eu

pl_ena=/root/bin/plugin-enable.sh

${pl_ena} http_loadtime http_loadtime

rm -vf /etc/munin/plugins/mongo*
#~ ${pl_ena} contrib mongodb/mongodb_conn mongodb_conn
#~ ${pl_ena} contrib mongodb/mongodb_docs mongodb_docs
#~ ${pl_ena} contrib mongodb/mongo_lag mongo_lag
#~ ${pl_ena} contrib mongodb/mongo_mem mongo_mem
#~ ${pl_ena} contrib mongodb/mongo_ops mongo_ops

rm -vf /etc/munin/plugins/uwsbot_stats
###ln -svf /uws/bin/uwsbot-stats /etc/munin/plugins/uwsbot_stats

rm -vf /etc/munin/plugins/api*
#~ ln -svf /uws/bin/api-job-stats /etc/munin/plugins/api_job_stats

exit 0
