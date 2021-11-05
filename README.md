**Steps to build the development environment**

- git clone git@gitlab.com:mehdifth/platform.git , here the public ssh keys must be already loaded in the gitlab
- mv platform docker_iot

- vi Dockerfile
- add these contents:
FROM debian:buster
RUN apt-get update
RUN apt-get -y install ntp ssh vim net-tools python3 python3-pip wget
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN cat ./bashrc_append >> /root/.bashrc
CMD tail -f /dev/null


- docker build -t debian_iot_image .

- docker run -d -p2222:22 -p8080:8080 -p4343:4343 --shm-size 2g --privileged -v /Users/amc/Desktop/G/Docker/docker_iot:/opt/source debian_iot_imag
- Note: /Users/amc/Desktop/G/Docker/docker_iot is the address of the cloned git repo

- Find the container id with “docker ps -a”

- docker exec -it a5ff9cec9f2e /bin/bash



