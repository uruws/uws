#!/bin/sh
set -eu
/opt/uws/venv/bin/python3 -m compileall /opt/uws/chatbot/*.py
exec /opt/uws/venv/bin/python3 /opt/uws/chatbot/chatbot_main.py
