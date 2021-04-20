#!/bin/sh
set -eu
app=${1:?'app env?'}
build_dir=/srv/heroku

rm -vfr ${build_dir}/Dockerfile ${build_dir}/utils
cp -va ./pod/heroku/Dockerfile ${build_dir}/
cp -va ./pod/heroku/utils ${build_dir}/

cd ${build_dir}
exec docker build --rm --build-arg APP=${app} -t uwspod/heroku .
