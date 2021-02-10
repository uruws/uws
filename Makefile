.PHONY: default
default: bootstrap

.PHONY: clean
clean:
	@rm -rvf ./tmp

.PHONY: prune
prune:
	@docker system prune -f

.PHONY: upgrade
upgrade:
	@./docker/base/build.sh --pull
	@./docker/awscli/build.sh --pull
	@$(MAKE) all

.PHONY: bootstrap
bootstrap: base awscli mkcert

.PHONY: base
base:
	@./docker/base/build.sh

.PHONY: awscli
awscli:
	@./docker/awscli/build.sh

.PHONY: mkcert
mkcert:
	@./docker/mkcert/build.sh

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
	@./docker/ecr-push.sh awscli
	@./docker/ecr-push.sh mkcert
	@./docker/ecr-push.sh munin

.PHONY: ecr-login
ecr-login:
	@./docker/ecr-login.sh

.PHONY: deploy
deploy: clean prune
	@echo "i - START deploy `date -R`"
	@./env/make.sh prod all
	@./host/ecr-login.sh
	@./env/make.sh prod publish
	@./host/deploy.sh local janis
	@echo "i - END deploy `date -R`"
