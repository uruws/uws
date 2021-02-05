ENV ?= dev

.PHONY: default
default: bootstrap

.PHONY: env
env:
	@echo "ENV=$(ENV)" >.env

.PHONY: bootstrap
bootstrap: base awscli

.PHONY: all
all: bootstrap acme munin

.PHONY: ecr-login
ecr-login:
	@./docker/ecr-login.sh

.PHONY: publish
publish: all
	@./docker/ecr-push.sh base
	@./docker/ecr-push.sh acme
	@./docker/ecr-push.sh munin

.PHONY: upgrade
upgrade:
	@./docker/base/build.sh --pull
	@./docker/awscli/build.sh --pull
	@$(MAKE) all

.PHONY: prune
prune:
	@docker system prune -f

.PHONY: base
base:
	@./docker/base/build.sh

.PHONY: awscli
awscli:
	@./docker/awscli/build.sh

.PHONY: acme
acme: base
	@./acme/build.sh

.PHONY: munin
munin: base
	@./munin/build.sh
