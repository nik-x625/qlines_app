**Current Architecture**
- Apache => WSGI => Flask
- Redis is involved for message queue use cases


**Steps to build the development environment****
- git clone git@gitlab.com:mehdifth/platform.git
- Note: here the public ssh keys must be already loaded in the gitlab
- mv platform docker_iot
- cd docker_iot
- Now the content of the file Dockerfile will be executed
- docker build -t debian_iot_image .
- docker run -d -p2222:22 -p8080:8080 -p4343:4343 --shm-size 2g --privileged -v /Users/amc/Desktop/G/Docker/docker_iot:/opt/source debian_11_iot_image
- Note: /Users/amc/Desktop/G/Docker/docker_iot is the address of the cloned git repo
- Find the container id with “docker ps -a”
- docker exec -it a5ff9cec9f2e /bin/bash  
- or use the alias "iot", for this you need to define this alias in mac as below:
- in Mac, in the file ~/.zprofile, add this:
- alias iot="docker exec -it $(docker ps  | grep 'debian_iot' | awk '{print $1}') /bin/bash"


**Deployment to cloud vps**
add this to the apache config: python-path=/var/www/site_platx:/usr/local/lib/python3.7/dist-packages
change the logger file path:
- edit the file logger_custom.py
- change from "/opt/source/mylogs.log" to "/var/www/site_platx/mylogs.log"
- in apache might be needed to remove the tags: `<IfDefine IgnoreBlockComment> and </IfDefine>`


**What to remember about Redis and message queue**
- install the redis-server on both linux and python by "apt-get install redis" and "pip3 install redis"
- use this in the main python script:
```
import redis
from rq import Queue
r = redis.Redis()
q = Queue('platx', connection=r)
```

- create rqworker.py with this content:
```
#!/usr/bin/env python
import os

import redis
from rq import Worker, Queue, Connection

listen = ['platx']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()

```

- if you want to put into the queue, do like this:
```result = q.enqueue(yourmetho, inputs_to_the_metho)```

