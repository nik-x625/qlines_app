Steps to build the development environment**

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


Architecture
Apache => WSGI => Flask