# kubernetes nginx vs heroku

Comparison between aws k8s nginx setup with heroku's.

Using [selenium tests](./testing/app) ran using [flood.io](https://app.flood.io) platform.

# Heroku

* [loginTeachersHeroku 3][loginTeachersHeroku 3]
	* 1 dyno: mem 1024
	* no errors reported by flood but we can see some 5xx and mem issues reported by heroku
	* response times around 11s
	* it seems that heroku router's keeps a "connections pool" or some similar wainting for the dyno(s) to be ready for the next request.

[loginTeachersHeroku 3]: https://app.flood.io/projects/121440/flood/2IMbjWNT8HkxJX2aoHmg754Cgjy/grid/5TIl7NU5YvbBcdbupv8iHQ/timeline/2022-12-02T15:22:30.000Z/2022-12-02T15:37:45.000Z


* [loginTeachersHeroku 5][loginTeachersHeroku 5]
	* 2 dynos: mem 1024
	* still some 5xx and mem issues reported on heroku's metrics graphs
	* response times around 6s
	* using two dynos drops down response times to half, so it makes sense with the "connections pool" theory

[loginTeachersHeroku 5]:
https://app.flood.io/projects/121440/flood/2IV5dltx3IVUsLiq8ckVN20WTZB/grid/GpNfcJfV3OPoTSwtyXYxeQ/timeline/2022-12-05T15:27:30.000Z/2022-12-05T15:42:15.000Z
