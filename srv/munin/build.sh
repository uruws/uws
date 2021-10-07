#!/bin/sh
set -eu
buildd=${PWD}/srv/munin/build
mkdir -vp ${buildd}
install -v -C ${PWD}/python/lib/sendmail.py ${buildd}/sendmail.py
exec docker build $@ --rm -t uws/munin ./srv/munin
