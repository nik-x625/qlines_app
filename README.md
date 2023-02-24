**About current architecture**
- Apache => WSGI => Flask
- Redis is involved for message queue use cases
- "Init scripts" are used. So far ok but need to make a better approach for Docker.
- Dockerfile will be updated with the configuration steps
- For tests (on python packages or OS packages) use current container, the Dockerfile helps to create from scratch later
- Using VSCODE in the docker folder in Mac local filesystem, then docker in the VPS
- Using aliases inside the container, use aliases outisde the container
- Clickhouse and Mosquitto only enabled in lab for the moment, refer to notes to install


**Steps to build the environment - both test and prod**
- install docker engine on the production linux server. Ref: https://docs.docker.com/engine/install/debian/, start from the step "Set up the repository"
- in case of Mac, go to the Docker folder of the Mac, probably it is in this folder: /Users/amc/Desktop/G/Docker
- git clone git@github.com:mehdifth/platform.git  (note: Github must already have the ssh public keys)
- rename the platform to "qlines" to be able to use more apps with this platform
- mv platform qlines
- mkdir platform
- mv qlines ./platform/
- now there is one platform folder which could include folders like qlines, app1, app2, ...
- cd ./platform
- docker build -t debian_platform_image_v1 ./qlines/
- in dev platform: docker run -d -p80:80 -p443:443 -p 7000-7100:7000-7100 --shm-size 2g --privileged -v "$(pwd)":/opt/ debian_platform_image_v1
- in prod platform: docker run -d -p80:80 -p443:443 --restart always --shm-size 2g --privileged -v "$(pwd)":/opt/ debian_platform_image_v1
- docker exec -it a5ff9cec9f2e /bin/bash
- or use the alias "plt", for this you need to define this alias in mac/host as below:
- alias plt="docker exec -it $(docker ps  | grep 'debian_platform_image' | awk '{print $1}') /bin/bash"
- alias p="ps -ef | egrep 'apache|sql|mongo|python'"
- in each host, update the git outside the docker container. This way you will have the SSH key on the Git.
- install nodejs manually, follow this: https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-debian-10, refer to my iNotes for more details


**Deployment to production todos**
- enable the google analytics tag in all html filesystem
- Manage the SSL certificate/Letsencrypt 
As it was not possible to install in docker because of snapd, renew it in the host oustide of the docker container and move the files in /etc/letsencrypt to inside the docker.

Install NGINX outside of the container and use following config in /etc/nginx/sites-enable (no need to link from sites-available):

server {
        listen 80;
        listen [::]:80;

        root /var/www/your_domain/html;
        index index.html index.htm index.nginx-debian.html;

        server_name blog.qlines.net qlines.net www.qlines.net;

        location / {
                try_files $uri $uri/ =404;
        }
}

remove all other files in this folder
this covers all the 3 domains of "qlines.net", "www.qlines.net" and "blog.qlines.net"
then run the "certbot --nginx" outside of the docker container for 3 times
stop the nginx outside of the docker
copy the /etc/letsencrypt to inside the docker to /etc/letsencrypt
restart the nginx inside the docker
done!


- insdie docker, vi ~/.bashrc => change LAB to PROD in PS1
- inside docker, chmod 777 /opt/qlines/mylogs.log


**How the HA is designed
VM1: 
- LB1, Blog1, App1
VM2: 
- LB2, Blog2, App2
LB1 has a docker container to offload SSL and distribute the load, based on available app servers and subdomains (for blog versus app)
LB1 sees all the containers but sends only to 1. If one container fails sends the single one to 2
LB2 sees all the containers, but it is standby

DNS is switching between LB1 and LB2

High traffic will result in spawning the app containers. It means VM1 is big enough for this.
DB1 and DB2 are in separate VM servers because of sensitivies. All the nodes see DB1 and DB2 at the same time but send only to one of them.
TODO: Need arbiter here!

for MVP, I will go with big VM and backup/restore approach and later will have a sophisticated approach like above or use AWS!
for MVP, I will have nginx proxy in front (outside of containers) to SSL offload, route based on subnet (blog or app), etc.
Having 2 container behind it. Wordpress blog will use the official image with docker-compose: https://www.hostinger.com/tutorials/run-docker-wordpress





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
