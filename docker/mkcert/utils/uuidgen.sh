#!/bin/sh
set -eu
NAME=${1:?'cert name?'}
exec uuidgen --sha1 --namespace '@dns' --name "${NAME}"
