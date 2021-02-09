.PHONY: default
default: bootstrap

.PHONY: bootstrap
bootstrap: base awscli

.PHONY: upgrade
upgrade:
	@./docker/base/build.sh --pull
	@./docker/awscli/build.sh --pull
	@$(MAKE) all

.PHONY: clean
clean:
	@rm -rvf ./tmp

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
	@./srv/acme/build.sh

.PHONY: munin
munin: base
	@./srv/munin/build.sh

.PHONY: all
all: bootstrap acme munin

.PHONY: publish
publish: all
	@./docker/ecr-push.sh base
	@./docker/ecr-push.sh acme
	@./docker/ecr-push.sh munin

.PHONY: ecr-login
ecr-login:
	@./docker/ecr-login.sh

.PHONY: deploy
deploy:
	@$(MAKE) awscli
#~ 	@$(MAKE) ecr-login
	@./env/make.sh prod all
	@./env/make.sh prod publish
	@./host/deploy.sh local janis
	@$(MAKE) clean prune
