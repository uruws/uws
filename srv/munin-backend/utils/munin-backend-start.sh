#!/bin/sh
set -eux

rm -vf /etc/apache2/sites-enabled/*
a2ensite 000-munin

rm -vf /var/log/apache2/*.log
ln -svf /dev/stderr /var/log/apache2/error.log
ln -svf /dev/stdout /var/log/apache2/access.log

apachectl -t
exec apachectl -D FOREGROUND
