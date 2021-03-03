AWS_REGION ?= us-east-1
DEPLOY_SERVER ?= janis

.PHONY: default
default: all

.PHONY: clean
clean:
	@rm -rvf ./build ./tmp ./docker/golang/tmp

.PHONY: distclean
distclean:
	@rm -rvf ./docker/golang/build ./docker/uwsbot/build ./srv/munin-node/build

.PHONY: prune
prune:
	@docker system prune -f

.PHONY: upgrade
upgrade:
	@./docker/base/build.sh --pull
	@./docker/awscli/build.sh --pull
	@$(MAKE) all

.PHONY: bootstrap
bootstrap: base acme mkcert uwspkg

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

.PHONY: uwsbot
uwsbot: base golang docker/uwsbot/build/uwsbot.bin docker/uwsbot/build/uwsbot-stats.bin
	@./docker/uwsbot/build.sh

docker/uwsbot/build/uwsbot.bin: docker/golang/build/uwsbot.bin
	@mkdir -vp ./docker/uwsbot/build
	@install -v docker/golang/build/uwsbot.bin ./docker/uwsbot/build/uwsbot.bin

docker/golang/build/uwsbot.bin:
	@./docker/golang/cmd.sh build -o /go/build/cmd/uwsbot.bin ./cmd/uwsbot

docker/uwsbot/build/uwsbot-stats.bin: docker/golang/build/uwsbot-stats.bin
	@mkdir -vp ./docker/uwsbot/build
	@install -v docker/golang/build/uwsbot-stats.bin ./docker/uwsbot/build/uwsbot-stats.bin

docker/golang/build/uwsbot-stats.bin:
	@./docker/golang/cmd.sh build -o /go/build/cmd/uwsbot-stats.bin ./cmd/uwsbot-stats

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
munin-node: base-testing srv/munin-node/build/uwsbot-stats.bin
	@./srv/munin-node/build.sh

srv/munin-node/build/uwsbot-stats.bin: docker/golang/build/uwsbot-stats.bin
	@mkdir -vp ./srv/munin-node/build
	@install -v docker/golang/build/uwsbot-stats.bin ./srv/munin-node/build/uwsbot-stats.bin

.PHONY: all
all: base base-testing awscli mkcert golang uwsbot uwspkg acme munin munin-backend munin-node

.PHONY: publish
publish: munin munin-backend munin-node
	@AWS_REGION=$(AWS_REGION) ./docker/ecr-push.sh munin
	@AWS_REGION=$(AWS_REGION) ./docker/ecr-push.sh munin-backend
	@AWS_REGION=$(AWS_REGION) ./docker/ecr-push.sh munin-node

.PHONY: ecr-login
ecr-login:
	@./docker/ecr-login.sh

.PHONY: deploy
deploy: clean distclean prune
	@echo "i - START deploy `date -R`"
	@$(MAKE) bootstrap
	@./host/ecr-login.sh $(AWS_REGION)
	@AWS_REGION=$(AWS_REGION) ./env/make.sh prod publish
	@./host/deploy.sh local $(DEPLOY_SERVER)
	@echo "i - END deploy `date -R`"
