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
quasi "regtest" mode. It's never been used in production either.
In its current state, this package can and should be used to experiment with
COALA IP.


## OK, how can I start experimenting?

1. Read the installation section on how to install with Docker.
2. Get familiar with the REST API provided at the end of this document.
3. Hit against a running docker container with a HTTP client of your choice.


## Should I expose this server to the internet?

NO! Think of this library more like a shell-command. The flask server should at
least be run behind a reverse-proxy like nginx, so that it's interface is NOT
exposed to the world wide web.


## Can I just have a shell-command for this?

Yes, [curl](https://curl.haxx.se/).


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


### Create Users

This call will not store any data on the running instance of BigchainDB.
It simply generates a verifying and signing key-pair that can be used in a
POST-manifestation call.

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


### Register a Manifestation

In order to register the manifestation on BigchainDB as transactions on a
specific user's name, `verifyingKey` and `signingKey` need to be provided here.
The attributes shown for `manifestation` and `work` can be much more diverse,
for this see the COALA IP models definition (not yet publicly available yet).

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
        "author": "J. R. R. Tolkien",
    },
    "manifestation": {
        "@id": "<currently empty>",
        "name": "The Fellowship of the Ring",
        "manifestationOfWork": "<URI pointing to the Work's transaction ../<txid>",
        "datePublished": "29-07-1954",
        "url": "<URI pointing to a media blob>",
        "isManifestation": true,
    },
    "copyright": {
        "@id": "<currently empty>",
        "rightsOf": "<Relative URI pointing to the Manifestation ../<txid>",
    },
}
```

#### Why is `@id` currently empty?

We're planning to replace JSON-LD's URI linking structure with
[IPLD](https://github.com/ipld/specs). As it's not fully implemented in
BigchainDB yet, `@id` is empty for now.


#### Was my POST to `/manifestations/` successful?

To check if your POST was successful, try validating by doing the following:

1. Check the response of your POST request: Is the return value similar to the
   example provided above?

or

[@Sohkai plz change PORT if necessary]

1. Open your browser and go to `http://localhost:9984/api/v1` (your locally
   running BigchainDB instance)

2. To check if your previously created models were included in BigchainDB, take
   the string in `manifestationOfWork` or `rightsOf` and append it to the
   following link: `http://localhost:9984/api/v1/transactions/<string goes here>`.
   BigchainDB should then answer with the transaction, the model was registerd
   in.
