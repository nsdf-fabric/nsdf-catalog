# NSDF-Catalog

NSDF-Catalog provides an indexing service of known datasets/objects/files to an NSDF-Federation.

## Quickstart

The fastest way to get started is to use docker-compose:

    § docker-compose up

This spawns various containerized microserves which together form a NSDF-compatible indexing service.
An graphical overview is documented in (./docs/figures/overview.drawio).

It should now be possible to access a web frontend at:

    http://localhost:80/

And a REST API at:

    http://localhost:80/api/v1


## Production Deployment

It is highly recommended to run NSDF-catalog instances through a domain name for HTTPS.

 * (A domain to allow HTTPs via LetsEncrypt/Certbot)
 * A publically available IP
 * A machine (physical or virtual) to spawn multiple containers

