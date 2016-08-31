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

Of course not. Currently we're hitting against a BigchainDB instance running in
quasi "regtest" mode. It's never been used in production either.
In its current state, this package can and should be used to experiment with
COALA IP.


## OK, how can I start experimenting?

1. Read the installation section on how to install with Docker.
2. Get familiar with the REST API provided at the end of this document.
3. Hit against a running docker container with a HTTP client of your choice.


## Installation


### For development

```
$ git clone git@github.com:bigchaindb/coalaip-http-api.git
$ virtualenv --python=python3 venv
$ source venv/bin/activate
$ pip install -e .\[dev\] --process-dependency-links
$ python web/server.py
```

### For integration

Use Docker.


#### How to install Docker?
[@Sohkai plz add]


#### How to install and run COALA IP HTTP Wrapper with Docker
[@Sohkai plz add]


## REST API

## Create Users

```
POST /users/
HEADERS {"Content-Type": "application/json"}

PAYLOAD: None

RETURNS:
{
    "verifyingKey": "<base58 string>",
    "signingKey": "<base58 string>",
}
```

## Register a Manifestation

```
POST /manifestation/
HEADERS {"Content-Type": "application/json"}

PAYLOAD:
{
    "manifestation": {
        "name": "The Fellowship of the Ring",
        "datePublished": "29-07-1954",
        "url": "<URI pointing to a media blob>",
    },
    "user": {
        "verifyingKey": "<base58 string>",
        "signingKey": "<base58 string>",
    },
    "work": {
        "name": "The Lord of the Rings Triology",
        "author": "J. R. R. Tolkien",
    },
}


RETURNS:
{
    "work": {
        "@id": "<currently empty>",
        "name": "The Lord of the Rings Trilogy",
        "author": "<URI pointing to a Person or Organization object>",
    },
    "manifestation": {
        "@id": "<currently empty>",
        "name": "The Fellowship of the Ring",
        "isPartOf": "<URI pointing to the registered Work's transaction ../<txid>",
        "datePublished": "29-07-1954",
        "url": "<URI pointing to a media blob>",
        "isManifestation": true,
    },
    "copyright": {
        "@id": "<currently empty>",
        "rightsOf": "<Relative URI pointing to the registered Manifestation ../<txid>",
    },
}
```

