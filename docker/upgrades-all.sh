#!/bin/sh
set -eu

#-------------------------------------------------------------------------------
# base

# uws/base
./docker/upgrades.py -t uws/base

# uws/pod:base
./docker/upgrades.py -t uws/pod:base -U pod/base

# uws/awscli
./docker/upgrades.py -t uws/awscli

#-------------------------------------------------------------------------------
# utils

# uws/ansible
./docker/upgrades.py -t uws/ansible -U docker/asb
./docker/upgrades.py -t uws/ansible

# uws/golang
./docker/upgrades.py -t uws/golang -U docker/golang
./docker/upgrades.py -t uws/golang

# uws/python
./docker/upgrades.py -t uws/python -U docker/python
./docker/upgrades.py -t uws/python

# uws/cli
./docker/upgrades.py -t uws/cli -s uws/python -U docker/uwscli
./docker/upgrades.py -t uws/cli

# uws/uwsbot
./docker/upgrades.py -t uws/uwsbot -U docker/uwsbot
./docker/upgrades.py -t uws/uwsbot

# uws/mkcert
./docker/upgrades.py -t uws/mkcert -U docker/mkcert
./docker/upgrades.py -t uws/mkcert

# uws/mailx
./docker/upgrades.py -t uws/mailx -U docker/mailx
./docker/upgrades.py -t uws/mailx

# uws/k8s
./k8s/upgrades.py
./k8s/upgrades-all.sh
./docker/upgrades.py -t 'uws/${K8S_IMAGE}' || true

# uws/eks
./eks/upgrades.py
./eks/upgrades-all.sh
./docker/upgrades.py -t 'uws/${EKS_IMAGE}' || true

# uws/acme
./docker/upgrades.py -t uws/acme -U srv/acme
./docker/upgrades.py -t uws/acme

#-------------------------------------------------------------------------------
# services

# uws/crond
./docker/upgrades.py -t uws/crond -s uws/mailx -U srv/crond
./docker/upgrades.py -t uws/crond

# uws/munin
./docker/upgrades.py -t uws/munin -s uws/mailx -U srv/munin
./docker/upgrades.py -t uws/munin

# uws/munin-backend
./docker/upgrades.py -t uws/munin-backend -s uws/munin -U srv/munin-backend
./docker/upgrades.py -t uws/munin-backend

# uws/munin-node
./docker/upgrades.py -t uws/munin-node -U srv/munin-node
./docker/upgrades.py -t uws/munin-node

# uws/nginx
./docker/upgrades.py -t uws/nginx -U srv/nginx
./docker/upgrades.py -t uws/nginx

# uws/proftpd
./docker/upgrades.py -t uws/proftpd -U srv/proftpd
./docker/upgrades.py -t uws/proftpd

#-------------------------------------------------------------------------------
# webapps

# uws/webapp
./docker/upgrades.py -t uws/webapp -U docker/webapp
./docker/upgrades.py -t uws/webapp
./docker/upgrades.py -t 'uws/${webapp}' || true

# uws/ab
./docker/upgrades.py -t uws/ab -s uws/webapp -U srv/ab
./docker/upgrades.py -t uws/ab

# uws/chatbot
./docker/upgrades.py -t uws/chatbot -s uws/webapp -U srv/chatbot
./docker/upgrades.py -t uws/chatbot

# uws/admin
./docker/upgrades.py -t uws/admin -s uws/webapp -U srv/admin
./docker/upgrades.py -t uws/admin

exit 0
