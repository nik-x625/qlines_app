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
- Grafana running on port 8082 (temporary)


**Steps to build the environment - both Testbed and Production**
- install docker engine on the production linux server. Ref: https://docs.docker.com/engine/install/debian/, start from the step "Set up the repository"
- In case of Mac, go to the Docker folder of the Mac, probably it is in this folder: /Users/amc/Desktop/G/Docker
- git clone git@gitlab.com:mehdifth/platform.git  (note: Gitlab must already have the ssh public keys)
- rename the platform to "qlines" to be able to use more apps with this platform
- mv platform qlines
- mkdir platform
- mv qlines ./platform/
- now there is one platform folder which could include folders like qlines, app1, app2, ...
- cd ./platform
- docker build -t debian_platform_image ./qlines/  (the Dockerfile content is read here)
- docker run -d -p80:80 -p8080:8080 -p8081:8081 -p 8082:8082 -p443:443 --shm-size 2g --privileged -v "$(pwd)":/opt/ --restart=always debian_platform_image
- now the docker container and the app should be running
- Find the container id with "docker ps -a"
- docker exec -it a5ff9cec9f2e /bin/bash
- or use the alias "iot", for this you need to define this alias in mac/host as below:
- alias iot="docker exec -it $(docker ps  | grep 'debian_platform' | awk '{print $1}') /bin/bash"
- alias iotc="cd /opt/platform/qlines"
- alias p="ps -ef | egrep 'apache|sql|mongo|python'"
- in each host, enter the "iotc" and update the git. This way you will have the SSH key on the Git.
- to change the command line prompt for easier readings, edit ~/.bashrc file and change PS1 entry based on LAB or PROD environment.


**Deployment to cloud vps** => deprecated because the production now is on Docker too, it is valid for chroot cases
- add this to the apache config: 
- python-path=/var/www/site_platx:/usr/local/lib/python3.7/dist-packages
- change the logger file path. edit the file logger_custom.py and change from "/opt/qlines/mylogs.log" to "/var/www/site_platx/mylogs.log"
- in apache might be needed to remove the tags: `<IfDefine IgnoreBlockComment> and </IfDefine>`


**What to remember about Redis and message queue**
- install the redis-server on both linux and python by "apt-get install redis" and "pip3 install redis"
- use this in the main python script where you want to push the jobs to queue:
```
import redis
from rq import Queue
r = redis.Redis()
q = Queue('app1', connection=r)
```

- create rqworker.py with this content:
```
#!/usr/bin/env python
import os

import redis
from rq import Worker, Queue, Connection

listen = ['app1']
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

- "yourmethod" is the method to consume the object in the queue, and "inputs_to_the_metho" is the input for that method. "app1" is the pipe name in the queue.
- for more queues, it is enough to expand this list for more items:
```listen = ['app1']```
