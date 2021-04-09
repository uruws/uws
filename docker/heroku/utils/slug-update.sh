#!/bin/sh
set -eu
echo "SLUG UPDATE: $@"
APP=${1:?'app name?'}

cd /home/uws/download

heroku slugs -a ${APP} | head >${APP}-slugs.head
cat ${APP}-slugs.head | grep -E '^v[[:digit:]]+: ' |
	head -n1 | cut -d ' ' -f 2 >${APP}.new

if test -s ./${APP}.cur; then
	slug_cur=$(cat ${APP}.cur)
	slug_new=$(cat ${APP}.new)
	if test "X${slug_new}" = "X${slug_cur}"; then
		echo "${APP}: no new slug..."
		exit 0
	fi
fi

heroku config -s -a ${APP} >${APP}.env.new
cat ${APP}.env.new | sed 's#^#export #' >${APP}.env
rm -vf ${APP}.env.new

echo "${APP}: update slug ${slug_new}"
heroku slugs:download -a "${APP}" "${slug_new}"
rm -vf ${APP}/slug.tar.gz

exit 0
