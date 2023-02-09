#!/bin/sh
set -eu

#~ # nginx.env
#~ uwskube delete secret proxy-env -n nginx || true
#~ uwskube create secret generic proxy-env -n nginx \
	#~ --from-env-file=${HOME}/cluster/nginx.env

# sites-enabled
uwskube delete secret sites-enabled -n nginx || true
uwskube create secret generic sites-enabled -n nginx \
	--from-file=${HOME}/cluster/nginx/sites-enabled

# tapo tls
uwskube delete secret tapo-tls -n nginx || true
uwskube create secret tls tapo-tls -n nginx \
	--cert=${HOME}/ca/godaddyCerts/bundled_all.crt \
	--key=${HOME}/ca/godaddyCerts/server.key

exit 0
