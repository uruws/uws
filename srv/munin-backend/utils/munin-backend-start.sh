#!/bin/sh
set -eu

if test -d /efs/munin-db; then
	install -v -d /efs/munin-db/data/munin-db
	rm -rf /var/lib/munin
	ln -sv /efs/munin-db/data/munin-db /var/lib/munin
	install -v -d /var/lib/munin/cgi-tmp
else
	install -v -d -m 0775 -o munin -g www-data /var/lib/munin/cgi-tmp
fi

if test -d /efs/munin-cache; then
	install -v -d /efs/munin-cache/data/munin-cache
	rm -rf /var/cache/munin/www
	ln -sv /efs/munin-cache/data/munin-cache /var/cache/munin/www
fi

rm -rf /var/lib/munin/cgi-tmp/*

rm -vf /etc/apache2/sites-enabled/*
a2ensite 000-munin

rm -vf /var/log/apache2/*.log
ln -svf /dev/stderr /var/log/apache2/error.log
ln -svf /dev/stdout /var/log/apache2/access.log

apachectl -t
exec apachectl -D FOREGROUND
