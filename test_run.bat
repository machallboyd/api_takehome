#!/bin/bash

ECHO Setting up docker api image
docker build -t api_takehome
docker run -d --name api_takehome -p 8000:8000 api_takehome

ECHO Activating API
curl http://127.0.0.1:8000/csv

ECHO Requesting data from local database
