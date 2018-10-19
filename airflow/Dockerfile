# Base image
FROM python:2.7

# Image maintainer
LABEL maintainer="Aurelio Vivas <aa.vivas@uniandes.edu.co>"

# Airflow home directory
ENV AIRFLOW_HOME=/home/airflow

ENV AIRFLOW_GPL_UNIDECODE=yes

ENV SLUGIFY_USES_TEXT_UNIDECODE=yes

# Scripts folder for container confiurations
RUN mkdir -p /home/scripts

WORKDIR /home/scripts

COPY entrypoint.sh .

COPY requirements.txt .

# Update the index of available packages
RUN pip install -r requirements.txt

# Setting up the pwd of the container with it starts
WORKDIR /home/airflow

