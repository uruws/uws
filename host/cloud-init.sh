#!/bin/sh
set -eu

if test 'X--no-exec' != "X${1:-'X'}"; then
	exec ${0} --no-exec 2>&1 | tee -a /var/tmp/uws-deploy.log
fi

echo "i - START cloud-init $(date -R)"

st="$(cloud-init status 2>&1)"
if test "X${st}" != 'Xstatus: done' && test "X${st}" != 'Xstatus: not run' && test "X${st}" != 'Xstatus: error'; then
	echo "cloud-init invalid status: ${st}" >&2
	exit 1
fi

# fix cloud-init bug re-adding the same entry
(echo 'admin ALL=(ALL) NOPASSWD:ALL'; echo 'uws ALL=(ALL) NOPASSWD:ALL') >/etc/sudoers.d/90-cloud-init-users
chmod -v 0440 /etc/sudoers.d/90-cloud-init-users

cloud-init clean
cloud-init init --local
cloud-init modules --mode config
cloud-init modules --mode final

chmod -v 0755 /etc/cloud/cloud.cfg.d/99zzzuws_setup.sh
/etc/cloud/cloud.cfg.d/99zzzuws_setup.sh

echo "i - END cloud-init $(date -R)"
exit 0
