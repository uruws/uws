#!/bin/sh
set -eu

# uws/base
./docker/upgrades.py -t uws/base

# uws/awscli
./docker/upgrades.py -t uws/awscli

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
./docker/upgrades.py -t uws/cli -U docker/uwscli -s uws/python
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

# uws/webapp
./docker/upgrades.py -t uws/webapp -U docker/webapp
./docker/upgrades.py -t uws/webapp

# uws/k8s
./k8s/upgrades.py
./k8s/upgrades-all.sh
./docker/upgrades.py -t 'uws/${K8S_IMAGE}' || true

# uws/eks
./eks/upgrades.py
./docker/upgrades.py -U docker/eks/124 -t uws/eks-124 -s uws/k8s-124
./docker/upgrades.py -t uws/eks-124        || true
./docker/upgrades.py -t 'uws/${EKS_IMAGE}' || true

# uws/acme
./docker/upgrades.py -t uws/acme -U srv/acme
./docker/upgrades.py -t uws/acme

# uws/crond
./docker/upgrades.py -t uws/crond -U srv/crond -s uws/mailx
./docker/upgrades.py -t uws/crond

# uws/munin
./docker/upgrades.py -t uws/munin -U srv/munin
./docker/upgrades.py -t uws/munin

# uws/munin-backend
./docker/upgrades.py -t uws/munin-backend -U srv/munin-backend -s uws/munin
./docker/upgrades.py -t uws/munin-backend

# uws/munin-node
./docker/upgrades.py -t uws/munin-node -U srv/munin-node
./docker/upgrades.py -t uws/munin-node

# uws/chatbot
./docker/upgrades.py -t uws/chatbot -U srv/chatbot -s uws/webapp
./docker/upgrades.py -t uws/chatbot

# uws/herokud
./docker/upgrades.py -t uws/herokud -U srv/herokud -s uws/crond
./docker/upgrades.py -t uws/herokud

# uws/nginx
./docker/upgrades.py -t uws/nginx -U srv/nginx
./docker/upgrades.py -t uws/nginx

# uws/proftpd
./docker/upgrades.py -t uws/proftpd -U srv/proftpd
./docker/upgrades.py -t uws/proftpd

# uws/ab
./docker/upgrades.py -t uws/ab -U srv/ab
./docker/upgrades.py -t uws/ab

exit 0
