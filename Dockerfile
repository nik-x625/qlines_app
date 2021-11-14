# buster or bullseye
FROM debian:buster
ENV TZ Europe/Berlin
RUN apt-get update -y
RUN apt-get -y install ntp ssh vim net-tools python3 python3-pip wget tzdata git apache2 tcpdump pylint
RUN apt-get -y install redis lsb-release

# Debian 10 (buster) => python 3.7
# Debian 11 (bullseye) => python 3.9
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN apt-get -y install libapache2-mod-wsgi-py3
RUN dpkg-reconfigure -f noninteractive tzdata
RUN pip3 install flask flask_login redis rq pymongo flake8
RUN useradd flask


# bashrc content
ADD _bashrc_append /tmp/
RUN cat /tmp/_bashrc_append >> /root/.bashrc


# apache config
ADD _apache_site.conf /tmp/
RUN cp /tmp/_apache_site.conf /etc/apache2/sites-available/000-default.conf
RUN echo "ServerName 127.0.0.1" >> /etc/apache2/apache2.conf
RUN a2enmod rewrite
RUN sed -i 's/Listen 80/Listen 8080/g' /etc/apache2/ports.conf


# git
RUN git config --global user.email "Mehdi's email from docker"
RUN git config --global user.name "Mehdi from docker"


# RQ worker init script
ADD _init_script_rq_worker_platx /tmp/
RUN cp /tmp/_init_script_rq_worker_platx /etc/init.d/rqworker


# MongoDB installation
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN apt update
RUN apt-get install gnupg2
RUN  wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org mongodb-org-database mongodb-org-server mongodb-org-shell mongodb-org-mongos mongodb-org-tools


# MongoDB init script
ADD _init_script_mongodb /tmp/
RUN cp /tmp/_init_script_mongodb /etc/init.d/mongodb
RUN chmod 755 /etc/init.d/mongodb


# all_daemons init script
ADD _init_script_all_daemons /tmp/
RUN cp /tmp/_init_script_all_daemons /etc/init.d/all_daemons
RUN chmod 755 /etc/init.d/all_daemons


# To keep container alive
CMD /etc/init.d/all_daemons restart;tail -f /dev/null
