AWS_REGION ?= us-east-1
DEPLOY_SERVER ?= janis

.PHONY: default
default: all

.PHONY: clean
clean:
	@rm -rvf ./build ./tmp

.PHONY: distclean
distclean: clean
	@rm -rvf ./docker/golang/tmp
	@rm -rvf ./docker/golang/build ./docker/uwsbot/build ./srv/munin-node/build

.PHONY: prune
prune:
	@docker system prune -f

.PHONY: upgrade
upgrade:
	@./docker/base/build.sh --pull
	@./docker/base-testing/build.sh
	@./docker/awscli/build.sh --pull

.PHONY: bootstrap
bootstrap: base base-testing golang acme mkcert awscli

.PHONY: base
base:
	@./docker/base/build.sh

.PHONY: base-testing
base-testing:
	@./docker/base-testing/build.sh

.PHONY: awscli
awscli:
	@./docker/awscli/build.sh

.PHONY: mkcert
mkcert:
	@./docker/mkcert/build.sh

.PHONY: golang
golang:
	@./docker/golang/build.sh

UWS_BOT_DEPS != find go/bot go/cmd/uwsbot* go/env go/config go/log -type f -name '*.go'

.PHONY: uwsbot
uwsbot: docker/uwsbot/build/uwsbot.bin docker/uwsbot/build/uwsbot-stats.bin docker/uwsbot/build/uwsbot.docs
	@./docker/uwsbot/build.sh

docker/uwsbot/build/uwsbot.bin: docker/golang/build/uwsbot.bin
	@mkdir -vp ./docker/uwsbot/build
	@install -v docker/golang/build/uwsbot.bin ./docker/uwsbot/build/uwsbot.bin

docker/golang/build/uwsbot.bin: $(UWS_BOT_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/uwsbot.bin ./cmd/uwsbot

docker/uwsbot/build/uwsbot-stats.bin: docker/golang/build/uwsbot-stats.bin
	@mkdir -vp ./docker/uwsbot/build
	@install -v docker/golang/build/uwsbot-stats.bin ./docker/uwsbot/build/uwsbot-stats.bin

docker/golang/build/uwsbot-stats.bin: $(UWS_BOT_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/uwsbot-stats.bin ./cmd/uwsbot-stats

docker/uwsbot/build/uwsbot.docs: $(UWS_BOT_DEPS)
	@mkdir -vp ./docker/uwsbot/build
	@./go/bot/gendocs.sh >./docker/uwsbot/build/uwsbot.docs

.PHONY: uwsbot-devel
uwsbot-devel: docker/uwsbot/build/uwsbot-devel.tgz

docker/uwsbot/build/uwsbot-devel.tgz: docker/uwsbot/build/uwsbot.bin docker/uwsbot/build/uwsbot-stats.bin docker/uwsbot/build/uwsbot.docs
	@rm -rfv ./docker/uwsbot/build/devel
	@mkdir -vp ./docker/uwsbot/build/devel/uws/bin ./docker/uwsbot/build/devel/uws/etc/env/bot
	@(cd ./docker/uwsbot/build \
		&& cp -va env/bot/bot/default env/bot/bot/staging env/bot/bot/stats \
			devel/uws/etc/env/bot/ \
		&& cp -va uwsbot.bin devel/uws/bin/uwsbot \
		&& cp -va uwsbot-stats.bin devel/uws/bin/uwsbot-stats \
		&& tar -cvzf uwsbot-devel.tgz -C devel .)

.PHONY: uwspkg
uwspkg:
	@./docker/uwspkg/build.sh

.PHONY: acme
acme:
	@./srv/acme/build.sh

.PHONY: munin
munin:
	@./srv/munin/build.sh

.PHONY: munin-backend
munin-backend:
	@./srv/munin-backend/build.sh

MUNIN_NODE_DEPS := srv/munin-node/build/uwsbot-stats.bin
MUNIN_NODE_DEPS += srv/munin-node/build/api-stats.bin
MUNIN_NODE_DEPS += srv/munin-node/build/apivsbot.bin
MUNIN_NODE_DEPS += srv/munin-node/build/api-job-stats.bin

.PHONY: munin-node
munin-node: $(MUNIN_NODE_DEPS)
	@./srv/munin-node/build.sh

srv/munin-node/build/uwsbot-stats.bin: docker/golang/build/uwsbot-stats.bin
	@mkdir -vp ./srv/munin-node/build
	@install -v docker/golang/build/uwsbot-stats.bin ./srv/munin-node/build/uwsbot-stats.bin

srv/munin-node/build/api-stats.bin: docker/golang/build/api-stats.bin
	@mkdir -vp ./srv/munin-node/build
	@install -v docker/golang/build/api-stats.bin ./srv/munin-node/build/api-stats.bin

srv/munin-node/build/apivsbot.bin: docker/golang/build/apivsbot.bin
	@mkdir -vp ./srv/munin-node/build
	@install -v docker/golang/build/apivsbot.bin ./srv/munin-node/build/apivsbot.bin

srv/munin-node/build/api-job-stats.bin: docker/golang/build/api-job-stats.bin
	@mkdir -vp ./srv/munin-node/build
	@install -v docker/golang/build/api-job-stats.bin ./srv/munin-node/build/api-job-stats.bin

.PHONY: heroku
heroku:
	@./docker/heroku/build.sh

.PHONY: heroku-logger
heroku-logger: docker/heroku/build/api-logs.bin docker/heroku/build/api-stats.bin
	@./docker/heroku/build-logger.sh

docker/heroku/build/api-logs.bin: docker/golang/build/api-logs.bin
	@mkdir -vp ./docker/heroku/build
	@install -v docker/golang/build/api-logs.bin docker/heroku/build/api-logs.bin

docker/heroku/build/api-stats.bin: docker/golang/build/api-stats.bin
	@mkdir -vp ./docker/heroku/build
	@install -v docker/golang/build/api-stats.bin docker/heroku/build/api-stats.bin

API_LOGS_DEPS != find go/api go/cmd/api* go/log go/fs -type f -name '*.go'
API_JOB_DEPS != find go/api go/cmd/api-job-stats go/log -type f -name '*.go'

docker/golang/build/api-logs.bin: $(API_LOGS_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/api-logs.bin ./cmd/api-logs

docker/golang/build/api-stats.bin: $(API_LOGS_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/api-stats.bin ./cmd/api-stats

docker/golang/build/apivsbot.bin: $(API_LOGS_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/apivsbot.bin ./cmd/apivsbot

docker/golang/build/api-job-stats.bin: $(API_JOB_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/api-job-stats.bin ./cmd/api-job-stats

# app-stats

APP_STATS_DEPS := go/cmd/app-stats/main.go go/app/stats/*.go

.PHONY: app-stats
app-stats: docker/golang/build/app-stats.bin

docker/golang/build/app-stats.bin: $(APP_STATS_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/app-stats.bin ./cmd/app-stats

.PHONY: clamav
clamav:
	@./docker/clamav/build.sh

.PHONY: k8s
k8s:
	@./docker/k8s/build.sh

.PHONY: eks
eks:
	@./docker/eks/build.sh

.PHONY: api
api: docker/golang/build/api-logs.bin docker/golang/build/apivsbot.bin
	@./srv/api/build.sh

.PHONY: proftpd
proftpd:
	@./srv/proftpd/build.sh

.PHONY: all
all: bootstrap uwsbot munin munin-backend munin-node proftpd

.PHONY: ecr-login
ecr-login:
	@./docker/ecr-login.sh

.PHONY: deploy
deploy:
	@echo "i - START deploy `date -R` as ${USER}"
	@$(MAKE) bootstrap k8s
	@./host/deploy.sh local $(DEPLOY_SERVER)
	@$(MAKE) prune
	@echo "i - END deploy `date -R`"
