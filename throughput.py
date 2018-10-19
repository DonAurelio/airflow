#!env/bin/python2.7
# -*- coding: utf-8 -*-

# Requirements 
# pip3 install psutil
# pip3 install requests

import psutil
import requests
import csv
import sys
import statistics
import datetime
import sys


TASK_SUCCESS = 'SUCCESS'
TASK_STARTED = 'STARTED'
TASK_RECEIVED = 'RECEIVED'
TASK_FAILED = 'FAILED'


# User must provides the HTTP URL of the FLOWER service 
# Ej: ./throughput 'http://172.24.99.218:8082'
FLOWER_API_URL = sys.argv[1] if len(sys.argv) > 1 else ''


def get_workers_data(**kwargs):

    endpoint = FLOWER_API_URL + '/api/workers'
    response = requests.get(url=endpoint)
    workers = response.json()

    worker_count = len(workers)

    # Mean of workers concurrency to test if all workers have the same 
    # concurrency 
    workers_concurrency = statistics.mean(
        [ int(w_data['stats']['pool']['max-concurrency']) for w_id, w_data in workers.items() ]
    )

    now = datetime.datetime.now()
    str_date = now.strftime("%Y-%m-%d %H:%M:%S")

    return str_date, worker_count, workers_concurrency

def get_tasks_data(**kwargs):
    
    endpoint = f'{FLOWER_API_URL}/api/tasks'
    response = requests.get(url=endpoint)
    tasks = response.json()

    task_count = len(tasks)
    received = 0  
    running = 0
    completed = 0
    falied = 0

    runtime = 0.0

    for task_id, data in tasks.items():
        completed += 1 if data['state'] in TASK_SUCCESS else 0
        running += 1 if data['state'] in TASK_STARTED else 0
        received += 1 if data['state'] in TASK_RECEIVED else 0
        falied += 1 if data['state'] in TASK_FAILED else 0

        runtime += float(data['runtime']) if data['state'] in TASK_SUCCESS else 0.0


    # Average running time of completed jobs
    avg_runtime = (runtime / completed) if completed != 0 else 0.0

    return received, running, completed, falied, avg_runtime


def get_system_data():

    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    cpu_percent = psutil.cpu_percent()

    return cpu_percent, memory_percent  


def write_data(file_name,*data):

    with open(file_name,'a') as csvfile:
        spamwriter = csv.writer(
            csvfile, delimiter=' ',
            quotechar='|', quoting=csv.QUOTE_MINIMAL
        )
        spamwriter.writerow(*data)

if __name__ == '__main__':
    data = ()
    data += get_workers_data()
    data += get_tasks_data()
    data += get_system_data()

    file_name = sys.argv[1] if len(sys.argv) > 1 else 'time.txt'

    header = (
        'Date'
        'Work.number',
        'Work.concurrency',
        'Task.received',
        'Task.running',
        'Task.completed',
        'T.falied',
        'Task.compl.runtime.avg',
        'CPU.usage (%)',
        'CPU.memory (%)'
    )

    write_data(file_name,data)
