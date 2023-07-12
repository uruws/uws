#!/bin/sh
set -u
uwskube delete svc munin-web -n mon --wait
~/ca/uws/smtps/teardown.sh mon
exit 0
