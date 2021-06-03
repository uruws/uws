.PHONY: all
all: uws general

.PHONY: uws
uws: uws/node-exporter.json

uws/node-exporter.json: Makefile
	@wget -c -O uws/node-exporter.json https://raw.githubusercontent.com/rfrail3/grafana-dashboards/master/prometheus/node-exporter-full.json
	@touch uws/node-exporter.json

.PHONY: general
general: nginx.json nginx-requests.json

nginx.json: Makefile
	@wget -c -O nginx.json https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/grafana/dashboards/nginx.json
	@touch nginx.json

nginx-requests.json: Makefile
	@wget -c -O nginx-requests.json https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/grafana/dashboards/request-handling-performance.json
	@touch nginx-requests.json
