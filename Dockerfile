FROM debian:buster
ENV TZ Europe/Berlin
RUN apt-get update -y
RUN apt-get -y install ntp ssh vim net-tools python3 python3-pip wget tzdata git
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN dpkg-reconfigure -f noninteractive tzdata
ADD bashrc_append /tmp/
RUN cat /tmp/bashrc_append >> /root/.bashrc
CMD tail -f /dev/null
