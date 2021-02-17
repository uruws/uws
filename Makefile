.PHONY: default
default: all

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
bootstrap: base base-testing awscli mkcert golang uwspkg

.PHONY: base
base:
	@./docker/base/build.sh

.PHONY: base-testing
base-testing: base
	@./docker/base-testing/build.sh

.PHONY: awscli
awscli:
	@./docker/awscli/build.sh

.PHONY: mkcert
mkcert: base
	@./docker/mkcert/build.sh

.PHONY: golang
golang: base-testing
	@./docker/golang/build.sh

.PHONY: uwspkg
uwspkg: base
	@./docker/uwspkg/build.sh

.PHONY: acme
acme: base
	@./srv/acme/build.sh

.PHONY: munin
munin: base-testing
	@./srv/munin/build.sh

.PHONY: munin-backend
munin-backend: munin
	@./srv/munin-backend/build.sh

.PHONY: munin-node
munin-node: base-testing
	@./srv/munin-node/build.sh

.PHONY: all
all: bootstrap acme munin munin-backend munin-node

.PHONY: publish
publish: munin munin-backend munin-node
	@./docker/ecr-push.sh munin
	@./docker/ecr-push.sh munin-backend
	@./docker/ecr-push.sh munin-node

.PHONY: ecr-login
ecr-login:
	@./docker/ecr-login.sh

.PHONY: deploy
deploy: clean prune
	@echo "i - START deploy `date -R`"
	@$(MAKE) bootstrap
	@./host/ecr-login.sh
	@./env/make.sh prod publish
	@./host/deploy.sh local janis
	@echo "i - END deploy `date -R`"
