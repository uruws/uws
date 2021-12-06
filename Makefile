AWS_REGION ?= us-east-1
DEPLOY_SERVER ?= janis

.PHONY: default
default: all

.PHONY: clean
clean:
	@rm -rvf ./build ./tmp

.PHONY: distclean
distclean: clean
	@rm -rvf ./docker/golang/build ./docker/golang/tmp
	@rm -rvf ./docker/k8s/build
	@rm -rvf ./docker/uwsbot/build
	@rm -rvf ./srv/munin-node/build

.PHONY: prune
prune:
	@docker system prune -f

.PHONY: upgrade
upgrade:
	@./docker/base/build.sh --pull
	@./docker/base-testing/build.sh
	@./docker/awscli/build.sh --pull

#
# all
#

.PHONY: all
all: bootstrap acme clamav k8sctl uwsbot munin munin-backend munin-node proftpd

#
# bootstrap
#

.PHONY: bootstrap
bootstrap: awscli base base-testing golang mkcert k8s eks python ansible uwscli

#
# base
#

.PHONY: base
base:
	@./docker/base/build.sh

.PHONY: base-testing
base-testing:
	@./docker/base-testing/build.sh

#
# utils
#

.PHONY: utils
utils: acme

.PHONY: utils-publish
utils-publish: utils
	@./docker/ecr-login.sh sa-east-1
	@./cluster/ecr-push.sh sa-east-1 uws/acme uwsops:acme

.PHONY: awscli
awscli:
	@./docker/awscli/build.sh

.PHONY: mkcert
mkcert:
	@./docker/mkcert/build.sh

.PHONY: golang
golang:
	@./docker/golang/build.sh

.PHONY: python
python:
	@./docker/python/build.sh

.PHONY: uwspkg
uwspkg:
	@./docker/uwspkg/build.sh

.PHONY: uwscli
uwscli:
	@./docker/uwscli/build.sh

.PHONY: acme
acme:
	@./srv/acme/build.sh

.PHONY: clamav
clamav:
	@./docker/clamav/build.sh

.PHONY: proftpd
proftpd:
	@./srv/proftpd/build.sh

.PHONY: ecr-login
ecr-login:
	@./docker/ecr-login.sh

.PHONY: ansible
ansible:
	@./docker/asb/build.sh

.PHONY: kali
kali:
	@./srv/kali/build.sh

#
# uwsbot
#

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

#
# api-job-stats
#

API_JOB_DEPS != find go/api go/cmd/api-job-stats go/log -type f -name '*.go'

docker/golang/build/api-job-stats.bin: $(API_JOB_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/api-job-stats.bin ./cmd/api-job-stats

#
# munin
#

.PHONY: munin-all
munin-all: munin munin-backend munin-node

.PHONY: munin
munin:
	@./srv/munin/build.sh

.PHONY: munin-backend
munin-backend:
	@./srv/munin-backend/build.sh

MUNIN_NODE_DEPS := srv/munin-node/build/uwsbot-stats.bin
MUNIN_NODE_DEPS += srv/munin-node/build/api-job-stats.bin

.PHONY: munin-node
munin-node: $(MUNIN_NODE_DEPS)
	@./srv/munin-node/build.sh

srv/munin-node/build/uwsbot-stats.bin: docker/golang/build/uwsbot-stats.bin
	@mkdir -vp ./srv/munin-node/build
	@install -v docker/golang/build/uwsbot-stats.bin ./srv/munin-node/build/uwsbot-stats.bin

srv/munin-node/build/api-job-stats.bin: docker/golang/build/api-job-stats.bin
	@mkdir -vp ./srv/munin-node/build
	@install -v docker/golang/build/api-job-stats.bin ./srv/munin-node/build/api-job-stats.bin

#
# heroku
#

.PHONY: heroku
heroku:
	@./docker/heroku/build.sh

#
# app-stats
#

APP_STATS_DEPS := go/cmd/app-stats/main.go go/app/stats/*.go

.PHONY: app-stats
app-stats: docker/golang/build/app-stats.bin

docker/golang/build/app-stats.bin: $(APP_STATS_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/app-stats.bin ./cmd/app-stats

#
# deploy
#

.PHONY: deploy
deploy:
	@echo "i - START deploy `date -R` as ${USER}"
	@$(MAKE) bootstrap check
	@./host/deploy.sh local $(DEPLOY_SERVER)
	@$(MAKE) prune
	@echo "i - END deploy `date -R`"

#
# check
#

.PHONY: check
check: check-cli check-munin check-k8s

.PHONY: check-cli
check-cli:
	@echo '*** cli/test/run/shellcheck.sh'
	@./docker/uwscli/cmd.sh ./test/run/shellcheck.sh
	@echo '*** cli/test/run/vendor.sh'
	@./docker/uwscli/cmd.sh ./test/run/vendor.sh
	@echo '*** cli/test/run/coverage.sh'
	@./docker/uwscli/cmd.sh ./test/run/coverage.sh

.PHONY: check-munin
check-munin:
	@./srv/munin/check.sh

.PHONY: check-k8s
check-k8s:
	@echo '*** k8s/test/run/shellcheck.sh'
	@./docker/k8s/devel.sh ./k8s/test/run/shellcheck.sh
	@echo '*** k8s/test/run/coverage.sh'
	@./docker/k8s/devel.sh ./k8s/test/run/coverage.sh

#
# uws CA
#

.PHONY: CA
CA: mkcert
	@./secret/ca/uws/gen.sh ops
	@./secret/ca/uws/gen.sh smtps

#
# eks
#

.PHONY: eks
eks: k8s
	@./docker/eks/build.sh

#
# k8s
#

.PHONY: k8s
k8s: k8smon
	@./docker/k8s/build.sh

#
# k8smon
#

MON_TAG != cat ./k8s/mon/VERSION
MON_MUNIN_TAG != cat ./k8s/mon/munin/VERSION

.PHONY: mon-publish
mon-publish: awscli munin munin-backend munin-node
	@$(MAKE) k8smon-publish
	@./cluster/ecr-push.sh us-east-1 uws/munin uws:munin-$(MON_MUNIN_TAG)
	@./cluster/ecr-push.sh us-east-1 uws/munin-backend uws:munin-web-$(MON_MUNIN_TAG)
	@./cluster/ecr-push.sh us-east-1 uws/munin-node uws:munin-node-$(MON_MUNIN_TAG)

K8SMON_DEPS != find go/cmd/k8smon go/k8s/mon -type f -name '*.go'

.PHONY: k8smon
k8smon: docker/k8s/build/k8smon.bin

docker/k8s/build/k8smon.bin: docker/golang/build/k8smon.bin
	@mkdir -vp ./docker/k8s/build
	@install -v docker/golang/build/k8smon.bin ./docker/k8s/build/k8smon.bin

docker/golang/build/k8smon.bin: $(K8SMON_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/k8smon.bin ./cmd/k8smon

.PHONY: k8smon-publish
k8smon-publish: k8s
	@./docker/ecr-login.sh us-east-1
	@./cluster/ecr-push.sh us-east-1 uws/k8s uws:mon-k8s-$(MON_TAG)

#
# k8sctl
#

CTL_TAG != cat ./k8s/ctl/VERSION

.PHONY: k8sctl
k8sctl: eks

.PHONY: k8sctl-publish
k8sctl-publish: k8sctl
	@./docker/ecr-login.sh us-east-1
	@./cluster/ecr-push.sh us-east-1 uws/eks-k8s uws:ctl-eks-$(CTL_TAG)
