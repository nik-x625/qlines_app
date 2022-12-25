**About current architecture**
- Apache => WSGI => Flask
- Redis is involved for message queue use cases
- "Init scripts" are used. No need to switch to "systemd". So far they work fine.
- Dockerfile will be updated with the configuration steps
- For tests (on python packages or OS packages) use current container, the Dockerfile helps to create from scratch later
- using rq worker as init script
- using redis as init script
- using VSCODE in the docker folder in Mac local filesystem, then docker in the VPS
- use aliases inside the container, use aliases outisde the container
- Clickhouse and Mosquitto only enabled in lab for the moment, refer to notes to install


**Steps to build the environment - both test and prod**
- install docker engine on the production linux server. Ref: https://docs.docker.com/engine/install/debian/, start from the step "Set up the repository"
- In case of Mac, go to the Docker folder of the Mac, probably it is in this folder: /Users/amc/Desktop/G/Docker
- git clone git@gitlab.com:mehdifth/platform.git  (note: Gitlab must already have the ssh public keys)
- rename the platform to "qlines" to be able to use more apps with this platform
- mv platform qlines
- mkdir platform
- mv qlines ./platform/
- now there is one platform folder which could include folders like qlines, app1, app2, ...
- cd ./platform
- docker build -t debian_platform_image_v1 ./qlines/  (the Dockerfile content is read here)
- in dev platform: docker run -d -p80:80 -p443:443 -p 7000-7100:7000-7100 --shm-size 2g --privileged -v "$(pwd)":/opt/ debian_platform_image_v1
- in prod platform: docker run -d -p80:80 -p443:443 --restart always --shm-size 2g --privileged -v "$(pwd)":/opt/ debian_platform_image_v1
- now the docker container and the app should be running
- Find the container id with "docker ps -a"
- docker exec -it a5ff9cec9f2e /bin/bash
- or use the alias "platform", for this you need to define this alias in mac/host as below:
- alias platform="docker exec -it $(docker ps  | grep 'debian_platform_image' | awk '{print $1}') /bin/bash"
- alias p="ps -ef | egrep 'apache|sql|mongo|python'"
- in each host, update the git outside the docker container. This way you will have the SSH key on the Git.



**Deployment to production todos**
- add this to the apache config if necessary: python-path=/var/www/site_platx:/usr/local/lib/python3.7/dist-packages
- change the logger file path if necessary. edit the file logger_custom.py and change from "/opt/qlines/mylogs.log" to "/var/www/site_platx/mylogs.log"
- manage the apache tags if necessary: `<IfDefine IgnoreBlockComment> and </IfDefine>`
- enable the google analytics tag in all html filesystem
- install mosquitto and clickhouse manually for the moment


**Installing the ClickHouse**
- cd /tmp/
- curl https://clickhouse.com/ | sh
- ./clickhouse install
- vi /etc/clickhouse-server/config.xml and change the port from 8123 to something like 7010 which is exposed also in the container
- chown -R root:root /var/lib/clickhouse
- create /etc/clickhouse-server/config.d/docker_related_config.xml and add following content:
```
<clickhouse>
     <!-- Listen wildcard address to allow accepting connections from other containers and host network. -->
    <listen_host>::</listen_host>
    <listen_host>0.0.0.0</listen_host>
    <listen_try>1</listen_try>

    <!--
    <logger>
        <console>1</console>
    </logger>
    -->
</clickhouse>
```

- run with command:
clickhouse-server --config-file /etc/clickhouse-server/config.xml --pid-file /var/run/clickhouse-server/clickhouse-server.pid --daemon
or use alias 'ch'



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
