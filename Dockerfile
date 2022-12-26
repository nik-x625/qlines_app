# buster or bullseye
FROM debian:bullseye
RUN apt-get update -y
RUN apt-get -y install ntp ssh vim net-tools python3 python3-pip wget tzdata git apache2
RUN apt-get -y install tcpdump tcpflow pylint iputils-ping curl unzip telnet redis lsb-release snapd

# enable SSL/HTTPS on Apache
RUN a2enmod ssl

# related to mysql
# RUN apt-get -y mysql-connector-python
# RUN pip3 install passlib


# Debian 10 (buster) => python 3.7
# Debian 11 (bullseye) => python 3.9
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
RUN apt-get -y install libapache2-mod-wsgi-py3
RUN pip3 install flask flask_login redis rq pymongo flake8 pyyaml markdown sqlalchemy flask_principal slugify feedwerk shortuuid psutil clickhouse_connect requests numpy
RUN useradd flask
RUN echo "Europe/Berlin" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# grafana packages
RUN apt-get -y install apt-transport-https software-properties-common


# This is necessary besides the main timezone command
RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime


# bashrc content
ADD DockerConfigFiles/_bashrc_append /tmp/
RUN cat /tmp/_bashrc_append >> /root/.bashrc


# apache config
ADD DockerConfigFiles/_apache_site.conf /tmp/
RUN cp /tmp/_apache_site.conf /etc/apache2/sites-available/000-default.conf
RUN echo "ServerName 127.0.0.1" >> /etc/apache2/apache2.conf
RUN a2enmod rewrite
#RUN sed -i 's/Listen 80/Listen 8080/g' /etc/apache2/ports.conf


# MongoDB installation
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN apt update
RUN apt-get -y install gnupg2
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list
RUN apt-get update
RUN apt-get -y install mongodb-org mongodb-org-database mongodb-org-server mongodb-org-shell mongodb-org-mongos mongodb-org-tools


# Required for python-ldap
#RUN apt-get -y install build-essential python3-dev python2.7-dev libldap2-dev libsasl2-dev slapd ldap-utils tox lcov valgrind
#RUN pip3 install python-ldap 


########### INIT SCRIPTS ###########
# RQ worker init script
ADD DockerConfigFiles/_init_script_rq_worker_platx /tmp/
RUN cp /tmp/_init_script_rq_worker_platx /etc/init.d/rqworker


# MongoDB init script
ADD DockerConfigFiles/_init_script_mongodb /tmp/
RUN cp /tmp/_init_script_mongodb /etc/init.d/mongodb
RUN chmod 755 /etc/init.d/mongodb

# Clickhouse init script
ADD DockerConfigFiles/_init_script_clickhouse /tmp/
RUN cp /tmp/_init_script_clickhouse /etc/init.d/clickhouse
RUN chmod 755 /etc/init.d/clickhouse

# Mosquitto init script
ADD DockerConfigFiles/_init_script_mosquitto /tmp/
RUN cp /tmp/_init_script_mosquitto /etc/init.d/mosquitto
RUN chmod 755 /etc/init.d/mosquitto

# all_daemons init script
ADD DockerConfigFiles/_init_script_all_daemons /tmp/
RUN cp /tmp/_init_script_all_daemons /etc/init.d/all_daemons
RUN chmod 755 /etc/init.d/all_daemons
########### INIT SCRIPTS ###########



# to enable logging in mylogs files
RUN touch mylogs.log
RUN chmod 777 mylogs.log


# To keep container alive
CMD /etc/init.d/all_daemons restart;tail -f /dev/null
