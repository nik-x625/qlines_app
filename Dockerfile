FROM debian:buster
RUN apt-get update
RUN apt-get -y install ntp ssh vim net-tools python3 python3-pip wget
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
CMD tail -f /dev/null
