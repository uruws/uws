#!/bin/sh
set -eu
exec helm get values -a haproxy-ingress
