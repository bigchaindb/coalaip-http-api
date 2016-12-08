# COALA IP HTTP Wrapper

> A HTTP wrapper for [pycoalaip](https://github.com/bigchaindb/pycoalaip).


## Why?

[pycoalaip](https://github.com/bigchaindb/pycoalaip) is Python-specific.
Furthermore all underlying dependencies are written in Python, which means
that parties interested in COALA IP would have to re-implement large parts of
their logic in their programming language to make use of COALA IP.
To solve this problem in the short-term, this library exposes a RESTful web
interface (runnable in Docker) of the functionalities provided in
[pycoalaip](https://github.com/bigchaindb/pycoalaip).


## Whats the status of this?

Super-pre-alpha. At the moment all you can do is hit against two endpoints that
are being exposed. Minimal error paths are provided.
This package and [pycoalaip](https://github.com/bigchaindb/pycoalaip)
will probably mature rather quickly as we're actively developing them
currently.


## Can I use this in production?

No. Currently we're hitting against a BigchainDB instance running in
quasi "regtest" mode. Its never been used in production either.
In its current state, this package can and should be used to experiment with
COALA IP.


## OK, how can I start experimenting?

1. Read the installation section on how to install with Docker.
1. Get familiar with the REST API provided at the end of this document.
1. Hit against a running Docker container with a HTTP client of your choice.


## Should I expose this server to the internet?

NO! Think of this library more like a shell-command. The flask server should at
least be run behind a reverse-proxy like nginx, so that its interface is NOT
exposed to the world wide web.


## Can I just have a shell-command for this?

Yes, [curl](https://curl.haxx.se/).


## Installation and Usage


### For development on Linux

1. You'll have to [install, configure and run BigchainDB as well as
RethinkDB](https://bigchaindb.readthedocs.io/en/latest/quickstart.html).

2. Install and run this library using the following commands:

```
$ git clone git@github.com:bigchaindb/coalaip-http-api.git
$ virtualenv --python=python3 venv
$ source venv/bin/activate
$ pip install -r requirements_dev.txt
$ python web/server.py
```


### For integration (or for non-Linux development)

Use Docker :whale:.


#### Installing Docker

You'll need to have at least the base [Docker](https://docs.docker.com/engine/installation/)
and [Docker Compose](https://docs.docker.com/compose/install/) installed, but
on some platforms (i.e. OSX and Windows), [Docker Machine](https://docs.docker.com/machine/install-machine/).
will also be necessary. As a quick primer, it may be interesting to go through
the guide to [run BigchainDB via Docker](http://bigchaindb-examples.readthedocs.io/en/latest/install.html#the-docker-way),
but we've already set up everything for you in this repo.

If you already have Docker installed, just make sure you have a recent version:

```bash
$ docker --version
Docker version 1.11.1, build 5604cbe

$ docker-compose --version
docker-compose version 1.7.0, build 0d7bf73
```

#### Running with Docker

Using the provided [docker-compose.yml](./docker-compose.yml), you can install
and start RethinkDB, BigchainDB, and the COALA IP HTTP server with just a
few commands.

First, copy the default environment settings and build the Docker containers:

```bash
$ cp .env_template .env
$ docker-compose build
```

And then start the services:

```bash
# In one terminal
# Note that BigchainDB must be started after RethinkDB has begun accepting connections (may take a few seconds)
$ docker-compose up -d rethinkdb
$ docker-compose up bigchaindb

# In another terminal
$ docker-compose up api
```

By default, the COALA IP HTTP server will now be available through
`http://localhost:3000/api/v1/`, along with the BigchainDB API
(`http://localhost:32768/api/v1/`) and the RethinkDB admin panel
(`http://localhost:58585`).

**Note**: If you are running Docker through Docker Machine, the services will
only be available through the hostname of your Docker Machine instance. Use
`docker-machine ip <machine-name>` to get this hostname, and use it to replace
the `localhost` part of the above URLs.

### Settings

The API server can be configured with a number of environment variables [see
.env_template](./.env_template).


## REST API


### Create Users

This call will not store any data on the running instance of BigchainDB.
It simply generates a verifying and signing key-pair that can be used in a
POST-manifestation call.

```
POST /api/v1/users/
HEADERS {"Content-Type": "application/json"}

PAYLOAD: None

RETURNS:
{
    "verifyingKey": "<base58 string>",
    "signingKey": "<base58 string>",
}
```


### Register a Manifestation

In order to register the manifestation on BigchainDB as transactions on a
specific copyright holder's name, the copyright holder's `verifyingKey` and
`signingKey` must be provided here.

Note that the attributes shown for `manifestation` and `work` can be much more
diverse; for this, see the COALA IP models definition (not yet publicly
available yet).

```
POST /api/v1/manifestations/
HEADERS {"Content-Type": "application/json"}

PAYLOAD:
{
    "manifestation": {
        "name": "The Fellowship of the Ring",
        "datePublished": "29-07-1954",
        "url": "<URI pointing to a media blob>"
    },
    "copyrightHolder": {
        "verifyingKey": "<base58 string>",
        "signingKey": "<base58 string>"
    },
    "work": {
        "name": "The Lord of the Rings Triology",
        "author": "J. R. R. Tolkien"
    }
}


RETURNS:
{
    "work": {
        "@id": "<Relative URI with the ID of the entity on BigchainDB>",
        "@type": "CreativeWork",
        "name": "The Lord of the Rings Trilogy",
        "author": "J. R. R. Tolkien"
    },
    "manifestation": {
        "@id": "<Relative URI with the ID of the entity on BigchainDB>",
        "@type": "CreativeWork"
        "name": "The Fellowship of the Ring",
        "manifestationOfWork": "<URI pointing to the Work's transaction ../<txid>",
        "datePublished": "29-07-1954",
        "url": "<URI pointing to a media blob>",
        "isManifestation": true
    },
    "copyright": {
        "@id": "<Relative URI with the ID of the entity on BigchainDB>",
        "@type": "Copyright"
        "rightsOf": "<Relative URI pointing to the Manifestation ../<txid>"
    }
}
```

#### What are the returned `@id`s?

The returned `@id`s denote the persisted ID of the entities on BigchainDB as a
relative URI to the current document base (i.e. the route URL, or
`/manifestations` in this case). For now, these point to the `CREATE`
transaction for the entity; in the future, they will be changing to be an asset
ID instead.

In the case of the returned Work and Copyright, their `@id`s are slightly
inconvenient to process as they live under a different base URL (`/works` and
`/rights`, respectively). You should strip away the leading paths to use just
the persisted IDs of these entities.

Note that in the future, we also plan to replace the JSON-LD linking structure
with [IPLD](https://github.com/ipld/specs).

#### Was my POST to `/manifestations/` successful?

To check if your POST was successful, try validating by doing the following:

1. Check the response of your POST request: Is the return value similar to the
   example provided above?

or

1. Open your browser and go to `http://localhost:9984/api/v1` (your locally
   running BigchainDB instance - if using the default Docker settings, use port
   `32768` instead).

1. To check if your previously created entities were included in BigchainDB,
   take the string in any of the returned `@id`s and append it to the following
   link: `http://localhost:9984/api/v1/transactions/<string goes here>`.
   BigchainDB should then answer with the transaction the entity was registered
   in (if using the default Docker settings, use port `32768` instead).

**Note**: If running on Docker and/or Docker Machine, substitute the hostnames
and ports of the above URLs with your Docker settings, as necessary (see the
[running with Docker section](#how-to-run-with-docker) for more help).


### Register a Right allowed by another Right or Copyright

Rather than registering new Rights directly to resulting rightsholders, new
Rights are initially registered to the current holder of the existing Right or
Copyright that allows for the new Right's creation. Doing so allows the initial
link between the source rightsholder and resulting rightsholder to be kept as
part of the new Right's chain of provenance.

Note that the attributes for the `right` may be much more diverse; see the COALA
IP models definition (not yet publicly available yet).

Also see transferring a Right on how to transfer a registered Right to new
holders.

```
POST /api/v1/rights/
HEADERS {"Content-Type": "application/json"}

PAYLOAD:
{
    "right": {
        "license": "<Legal license text or URI pointing to a license document>"
    },
    "currentHolder": {
        "verifyingKey": "<base58 string>",
        "signingKey": "<base58 string>"
    },
    "sourceRightId": "<ID of an existing Right that allows for the creation of this new Right>"
}

RETURNS:
{
    "right": {
        "@id": "<Relative URI with the ID of the entity on BigchainDB>",
        "@type": "Right",
        "allowedBy": <The sourceRightId>,
        "license": "<Legal license text or URI pointing to a license document>",
    }
}
```

To check if your POST was successful, follow the steps in [registering a
manifestation](#was-my-post-to-manifestations-successful) and use the returned
Right's data instead.
