#!/bin/sh
set -eu

shellcheck --color=auto ./eks/secrets/test/*.sh

shellcheck --color=auto ./eks/secrets/*.sh

find ./secret -type f -name '*.sh' -print0 |
	xargs --null -- shellcheck --color=auto

exit 0
