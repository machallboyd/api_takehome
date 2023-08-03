# Backend Engineering Take-Home Challenge

### Requirements
- Python 3.10+
- Docker
- PostgreSQL

## Introduction

A demo API for processing some csv data and writing it to a provided database.

Records:

1. Total experiments a user ran.
2. Average experiments amount per user.
3. User's most commonly experimented compound.

## Usage

### Setup

Make sure docker is running. Docker Desktop can be found at https://www.docker.com/products/docker-desktop/

Open a Unix terminal. On Mac, the the built-in Terminal application qualifies. On Windows, a convenient alternative is Windows Subsystem for Linux: https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-11-with-gui-support#1-overview

First, clone this repository into a local directory. In a terminal:

`git clone https://github.com/machallboyd/api_takehome.git`

Move to the root of the project directory:

`cd ./api_takehome`

To build an image of the API's docker container:

`docker build . -t api_takehome`

### Basic Test Usage

To create a container with the API running inside it, and exposed `8000` port:

`docker run -d --name api_takehome -p 8000:8000 api_takehome`

At this point, the API can be run with an ephemeral in-memory database for test purposes. However, the API container can be set up to use a container with a Postgres database instead.

### Usage with a Postgres database container

To run the API connected to a Postgres database container instead, first start a docker network that the two containers can communicate over:

`docker network create apinet`

Fetch a copy of the official postgres container image:

`docker pull postgres`

Create a container from the postgres image, passing in environment variables for the database name and default `postgres` user password. 

`docker run --name test_postgres -e POSTGRES_PASSWORD=extremely_secure_pw -e POSTGRES_DB=testdb -p 5432:5432 --net apinet -d postgres`

With the postgres database in place, as with the basic setup, build the API container and run it, but this time providing the name of the database container as an environment variable:

```bash
docker build . -t api_takehome
docker run -d --name api_takehome --net apinet -p 8000:8000 -e API_DB_PATH=test_postgres api_takehome
```

On launch, the API will attempt to connect to a container with the provided name over the docker network.

### Setting up the database

While the database could be configured manually at this point, the API has a convenience endpoint to set up the database it is connected to. This works for both the in-memory and postgres container databases

`curl http://localhost:8000/setup_test_db`

### Extracting, transforming and loading

With the database tables set up, the API endpoint to start the ETL process can be triggered with:

`curl http://localhost:8000/csv`

...processing the included csv files and saving the results to the connected database

### Reporting

The API also has a convenience endpoint for querying the database:

`curl http://localhost:8000/report`

This returns a JSON summary of the per-user data as well as the average number of tests run per user for the data set.

## Testing

The repository includes both a `bash` script to run through typical usage with a postgres database as well as a collection of unit tests.

### bash script

To trigger a script to create both containers, run the etl process, run the report, and tear down both containers, from the project's root directory:

`./test_run.sh`

### unit tests

To run the included tests locally, first create and activate a [Python 3.10 virtual environment](https://docs.python.org/3/library/venv.html).

With that virtual environment active, run:

```
pip install pip-tools
pip-sync dev-requirements.txt
```

The tests can now be run with

```
pytest .
```



