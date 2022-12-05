# kubernetes nginx vs heroku

Comparison between aws k8s nginx setup with heroku's.

Using [selenium tests](./../../testing/app) ran with [flood.io](https://app.flood.io) platform.

Tests using two ec2 m5.2xlarge instances, from San Pablo region (sa-east-1).

Test config:
	* 25 users per node (50 total)
	* during 15 minutes
	* users ramp up 5 minutes

# Heroku

Dynos with 1G of RAM still use swapping, which kubernetes _does not_. Some reports of __max__ memory used for 1G dynos are around __1.7G__.

* [loginTeachersHeroku 3][loginTeachersHeroku 3]
	* 1 dyno: mem 1024
	* no errors reported by flood
	* but we can see some 5xx and mem issues reported by heroku
	* response times around 11s
	* it seems that heroku router's keeps a "connections pool" or similar, waiting for the dyno(s) to be ready for the next request.

[loginTeachersHeroku 3]: https://app.flood.io/projects/121440/flood/2IMbjWNT8HkxJX2aoHmg754Cgjy/grid/5TIl7NU5YvbBcdbupv8iHQ/timeline/2022-12-02T15:22:30.000Z/2022-12-02T15:37:45.000Z


* [loginTeachersHeroku 5][loginTeachersHeroku 5]
	* 2 dynos: mem 1024
	* no errors reported by flood
	* still some 5xx and mem issues reported on heroku's metrics graphs
	* response times around 6s
	* using two dynos drops down response times to half, so it makes sense with the "connections pool" theory

[loginTeachersHeroku 5]:
https://app.flood.io/projects/121440/flood/2IV5dltx3IVUsLiq8ckVN20WTZB/grid/GpNfcJfV3OPoTSwtyXYxeQ/timeline/2022-12-05T15:27:30.000Z/2022-12-05T15:42:15.000Z

# k8s nginx

* [loginTeachers92 73][loginTeachers92 73]
	* 1 container: mem 2048
	* 125 rpm errors reported by flood: mostly 502s
	* connection timeout and connection refused errors observed in nginx logs during tests
	* the container was OOMKilled once during tests
		* that triggrers most of 502s as no container is available during restart
	* response times around 6s

[loginTeachers92 73]:
https://app.flood.io/projects/121440/flood/2IN3ViQiOy7Fb26d578uMZ5YI0a/grid/5TIl7NU5YvbBcdbupv8iHQ/timeline/2022-12-02T19:11:00.000Z/2022-12-02T19:26:15.000Z/notes

## References

* https://dev.to/bzon/nginx-ingress-load-balancing-and-retry-1008
* https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md
* https://nginx.org/en/docs/http/ngx_http_proxy_module.html
