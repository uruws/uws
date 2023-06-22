#!/bin/sh
set -eu
uwscb_ns=cb${UWSCB_ENV}
exec ~/pod/lib/rollin.sh "${uwscb_ns}" chatbot
