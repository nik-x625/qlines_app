#!/usr/bin/env python
import os

import redis
from rq import Worker, Queue, Connection
from logger_custom import get_module_logger
logger = get_module_logger(__name__)


listen = ['app1']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):

        worker = Worker(list(map(Queue, listen)))
        worker.work()
