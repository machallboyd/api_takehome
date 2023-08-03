#!/bin/bash
docker network create apinet

echo Setting up test db
docker pull postgres
docker run --name test_postgres -e POSTGRES_PASSWORD=extremely_secure_pw -e POSTGRES_DB=testdb --net apinet -d postgres

echo Setting up docker api image
docker build . -t api_takehome
docker run -d --name api_takehome --net apinet -p 8000:8000 -e API_DB_PATH=test_postgres api_takehome
sleep 2
./wait-for-it.sh -h 0.0.0.0 -p 8000

echo Activating API
curl http://localhost:8000/setup_test_db
curl http://localhost:8000/csv

echo Requesting data from local database
curl http://localhost:8000/report

echo Tearing down containers
docker rm -f test_postgres
docker rm -f api_takehome
