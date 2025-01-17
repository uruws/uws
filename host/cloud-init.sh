#!/bin/sh
set -eu

echo "i - START cloud-init $(date -R)"

st="$(cloud-init status 2>&1 || true)"
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

echo "i - END cloud-init $(date -R)"
exit 0
