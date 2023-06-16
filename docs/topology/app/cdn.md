# App CDN topology

          User---------.
           |           |
           |           |
           |           |
          CDN         App
    (abc123.c.n)   (app.t.o)
           |           |
           |           |
           |           |__ web and api containers
           |
           |________ nginx proxy cache
                     (appcdn.uws.t.o)
                            |
                            |
                            |
                        cdn containers

## Deploys

At deploy time the *cdn containers* MUST be deployed first in order to have the new assets ready for the CDN provider.

We now have the new assets ready for the CDN, but no *user* is asking for them yet; as *web and api containers* weren't deployed so far.

We have still the old asset's versions as well, in the nginx's cache (for 12hs). So *users* asking for either new versions or old versions will properly get them; either from the cache (old) or from the the new deployed *cdn containers*.

After *cdn containers* are ready, the *web and api containers* can be deployed.

## Refs

[nginx content caching](https://docs.nginx.com/nginx/admin-guide/content-cache/content-caching/)

## Why?

Because CDN providers do not retry if they get a 404 response, also on retrying they could still get a response from an old container during a deploy rolling out.
