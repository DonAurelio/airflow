#!/bin/bash 

# initialize the database
airflow initdb

# start the web server, default port is 8080
airflow webserver -p 8080 -D &

# start the scheduler
airflow scheduler -D &

# start the scheduler
airflow worker -D &

# flower service
airflow flower
