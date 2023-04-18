# CADD REST API Mocking Server

Mocking the CADD REST API server for VarFish development.

The server responds to requests like the original implementation and returns random numbers as scores.

## Setup

Create a Python environment of your choice, e.g. with conda.

```bash
# git clone https://github.com/bihealth/cadd-rest-api-mock
# cd cadd-rest-api-mock
# conda create -n cadd-rest-api-mock python=3.10
# conda activate cadd-rest-api-mock
# pip install Flask
```

## Use

The server will be listening on `localhost:5000`.

```bash
# flask --app mock run
```

In the VarFish `.env`, activate CADD. Make sure to include the protocol when pointing to the server.

```bash
VARFISH_ENABLE_CADD=1
VARFISH_CADD_REST_API_URL=http://localhost:5000
VARFISH_CADD_MAX_VARS=5000
```
