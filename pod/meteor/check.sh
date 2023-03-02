#!/bin/sh
set -eux

for fn in ./pod/meteor/*/deploy.sh; do
	grep -qF gw/deploy.sh "${fn}"
done

for fn in ./pod/meteor/*/restart.sh; do
	grep -qF gw/restart.sh "${fn}"
done

for fn in ./pod/meteor/*/rollin.sh; do
	grep -qF gw/rollin.sh "${fn}"
done

for fn in ./pod/meteor/*/scale.sh; do
	grep -qF gw/scale.sh "${fn}"
done
