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

# uws/acme
./docker/upgrades.py -t uws/acme -U srv/acme
./docker/upgrades.py -t uws/acme

# uws/mailx
./docker/upgrades.py -t uws/mailx -U docker/mailx
./docker/upgrades.py -t uws/mailx

# uws/webapp
./docker/upgrades.py -t uws/webapp -U docker/webapp
./docker/upgrades.py -t uws/webapp

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
./docker/upgrades.py -t uws/chatbot -U srv/chatbot
./docker/upgrades.py -t uws/chatbot

exit 0
