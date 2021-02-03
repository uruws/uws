.PHONY: default
default: bootstrap

.PHONY: bootstrap
bootstrap:
	@./docker/base/build.sh
	@./docker/awscli/build.sh

.PHONY: prune
prune:
	@docker system prune -f

.PHONY: all
all: bootstrap munin

.PHONY: munin
munin:
	@./munin/build.sh

.PHONY: publish
publish: all
	@./docker/ecr-login.sh
	@./docker/ecr-push.sh base
	@./docker/ecr-push.sh munin
