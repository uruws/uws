#!/bin/sh
set -eux

logfn=${1:?'logfile?'}
user=${2:?'user?'}
group=${3:-X}

srcd=/srv/mailx/etc
dstd=/etc/opt/mailx

if test 'XX' = "X${group}"; then
	group=${user}
fi

if test -s "${srcd}/aliases"; then
	install -v -m 0644 -o root -g root "${srcd}/aliases" "${dstd}/aliases"
fi

install -v -d -m 0755 -o root      -g root       "${dstd}"
install -v -d -m 0750 -o "${user}" -g "${group}" "${dstd}/${user}"

if test -s "${srcd}/msmtprc"; then
	dst=${dstd}/${user}
	install -v -m 0600 -o "${user}" -g "${group}" "${srcd}/msmtprc" "${dst}/msmtprc"
	if test 'Xsyslog' = "X${logfn}"; then
		echo 'logfile' >>"${dst}/msmtprc"
		echo 'syslog on' >>"${dst}/msmtprc"
	else
		echo "logfile ${logfn}" >>"${dst}/msmtprc"
		echo 'syslog off' >>"${dst}/msmtprc"
	fi
fi

exit 0
