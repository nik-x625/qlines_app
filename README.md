**Current Architecture**
- Apache => WSGI => Flask
- Redis is involved for message queue use cases
- "Init scripts" are used. No need to switch to "systemd". So far they work fine.
- Dockerfile will be updated with the configuration steps
- For tests (on python packages or OS packages) use current container, the Dockerfile helps to create from scratch later
- using rq worker as init script
- using redis as init script
- using VSCODE in the docker folder in Mac local filesystem, then docker in the VPS
- use aliases inside the container, use aliases outisde the container


**Steps to build the environment - both Testbed and Production
- git clone git@gitlab.com:mehdifth/platform.git
- Note: here the public ssh keys must be already loaded in the gitlab
- mv platform docker_iot
- cd docker_iot
- Now the content of the file Dockerfile will be executed
- docker build -t debian_iot_image .
- docker run -d -p80:80 -p443:443 --shm-size 2g --privileged -v "$(pwd)":/opt/source debian_iot_image
- Find the container id with “docker ps -a”
- docker exec -it a5ff9cec9f2e /bin/bash
- or use the alias "iot", for this you need to define this alias in mac as below:
- in the host where the docker engine is running add these aliases:
- alias iot="docker exec -it $(docker ps  | grep 'debian_iot' | awk '{print $1}') /bin/bash"
- alias iotc="docker exec -it $(docker ps  | grep 'debian_iot' | awk '{print $1}') /bin/bash"
- alias iotc="cd /Users/amc/Desktop/G/Docker/docker_iot"  => on Mac
- alias iotc="cd /opt/docker_iot" => on Linux host (vps)
- In each host, enter the "iotc" and update the git. This way you will have the SSH key on the Git.


**Deployment to cloud vps**
- add this to the apache config: 
- python-path=/var/www/site_platx:/usr/local/lib/python3.7/dist-packages
- change the logger file path. edit the file logger_custom.py and change from "/opt/source/mylogs.log" to "/var/www/site_platx/mylogs.log"
- in apache might be needed to remove the tags: `<IfDefine IgnoreBlockComment> and </IfDefine>`


**What to remember about Redis and message queue**
- install the redis-server on both linux and python by "apt-get install redis" and "pip3 install redis"
- use this in the main python script where you want to push the jobs to queue:
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
- the "rqworker.py" needs to be run always in the background, better to do with init script of systemd
- if you want to put into the queue, do like this:
```result = q.enqueue(yourmethod, inputs_to_the_metho)```

- "yourmethod" is the method to consume the object in the queue, and "inputs_to_the_metho" is the input for that method. "platx" is the pipe name in the queue.
- for more queues, it is enough to expand this list for more items:
```listen = ['platx']```


** In the production VPS, keep these aliases:
alias p="ps -ef | egrep 'apache|sql|mongo|python'"
alias iot="docker exec -it $(docker ps  | grep 'debian_iot_image' | awk '{print $1}') /bin/bash"
alias iotc="cd /opt/docker_iot"

