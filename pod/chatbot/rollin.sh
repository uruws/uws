#!/bin/sh
set -eu
ns=cb${UWSCB_ENV}
exec ~/pod/lib/rollin.sh "${ns}" chatbot
