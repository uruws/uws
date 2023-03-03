#!/bin/sh
set -eu

ignore_file() (
	fn=${1}
	case "${fn}" in
		./pod/meteor/api/*)
			return 0
		;;
		./pod/meteor/gw/*)
			return 0
		;;
		./pod/meteor/web/*)
			return 0
		;;
	esac
	return 1
)

for fn in ./pod/meteor/*/deploy.sh; do
	if ignore_file "${fn}"; then
		continue
	fi
	echo "grep -qF gw/deploy.sh ${fn}"
	grep -qF gw/deploy.sh "${fn}"
done

for fn in ./pod/meteor/*/restart.sh; do
	if ignore_file "${fn}"; then
		continue
	fi
	echo "grep -qF gw/restart.sh ${fn}"
	grep -qF gw/restart.sh "${fn}"
done

for fn in ./pod/meteor/*/rollin.sh; do
	if ignore_file "${fn}"; then
		continue
	fi
	echo "grep -qF gw/rollin.sh ${fn}"
	grep -qF gw/rollin.sh "${fn}"
done

for fn in ./pod/meteor/*/scale.sh; do
	if ignore_file "${fn}"; then
		continue
	fi
	echo "grep -qF gw/scale.sh ${fn}"
	grep -qF gw/scale.sh "${fn}"
done

for fn in ./pod/meteor/*/teardown.sh; do
	if ignore_file "${fn}"; then
		continue
	fi
	echo "grep -qF gw/teardown.sh ${fn}"
	grep -qF gw/teardown.sh "${fn}"
done

exit 0
