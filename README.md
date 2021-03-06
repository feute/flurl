# flurl
`flurl` is a very simple URL shortener.

It is meant to use with programs like `curl`.

You `POST` to `/` and get a response with a random string which is the
shortened URL.

It has only three endpoints:

- `GET /` to get the usage, similar to this README.
- `GET /<url>` to redirect to the original URL, if it exists.
- `POST /` to obtain a short URL (randomly generated) from the original one
taken from the `POST` data.

Behind the scenes, the server gets the original URL from the `POST` data,
uses the function `token_urlsafe` from the `secrets` package to generate
a random URL string, and saves the mapping in a database.

## Requirements

- `validators` package, install it with:

```
$ pip install validators
```

## Installation

```
$ pip install -e .
$ export FLASK_APP=flurl
$ flask initdb
$ flask run
```

## Usage

Assuming that the server is running on `localhost` port 5000.

```
$ curl localhost:5000
<usage>
$ curl -X POST -d <your-url> localhost:5000
<shortened url>
$ curl -L localhost:5000/<your-url>
<redirect to original url>
```
