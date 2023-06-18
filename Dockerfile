# buster or bullseye
FROM debian:bullseye
RUN apt-get update -y
RUN apt-get -y install ntp ssh vim net-tools python3 python3-pip python3-dev wget tzdata git nodejs npm sudo
RUN apt-get -y install tcpdump tcpflow pylint iputils-ping curl unzip telnet redis lsb-release snapd
RUN apt-get -y install mosquitto
RUN apt-get -y install build-essential libssl-dev libffi-dev python3-setuptools python3-venv
#RUN apt-get -y install nginx

# enable SSL/HTTPS on Apache
#RUN a2enmod ssl

# related to mysql
# RUN apt-get -y mysql-connector-python
# RUN pip3 install passlib

# Debian 10 (buster) => python 3.7
# Debian 11 (bullseye) => python 3.9
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
#RUN apt-get -y install libapache2-mod-wsgi-py3
RUN pip3 install flask flask_login redis rq pymongo flake8 pyyaml markdown sqlalchemy flask_principal slugify feedwerk shortuuid psutil clickhouse_connect requests numpy pandas paho-mqtt websockets
RUN useradd flask
RUN echo "Europe/Berlin" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN pip install jinja2==3.0

# for NGINX
RUN pip install gunicorn

# NGINX config
#COPY DockerConfigFiles/_nginx_qlines_main.conf /etc/nginx/sites-enabled/qlines_main.conf
#COPY DockerConfigFiles/_nginx_qlines_blog.conf /etc/nginx/sites-enabled/qlines_blog.conf


# grafana packages
RUN apt-get -y install apt-transport-https software-properties-common

# This is necessary besides the main timezone command
RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime

# bashrc content
COPY DockerConfigFiles/_bashrc_append /root/.bashrc

# Kafka requirements
RUN apt-get -y install default-jre
RUN apt-get -y install default-jdk
RUN curl "https://downloads.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz" -o /opt/kafka.tgz
RUN mkdir /opt/kafka && cd /opt/kafka && tar -xvzf /opt/kafka.tgz --strip 1
COPY DockerConfigFiles/_init_script_kafka /etc/init.d/kafka
RUN chmod 755 /etc/init.d/kafka
# apache config
#ADD DockerConfigFiles/_apache_site.conf /tmp/
#RUN cp /tmp/_apache_site.conf /etc/apache2/sites-available/000-default.conf

#RUN echo "ServerName 127.0.0.1" >> /etc/apache2/apache2.conf
#RUN a2enmod rewrite
#RUN sed -i 's/Listen 80/Listen 8080/g' /etc/apache2/ports.conf

# MongoDB installation
RUN cd /opt/
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN apt update
RUN apt-get -y install gnupg2
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list
RUN apt-get update
RUN apt-get -y install mongodb-org mongodb-org-database mongodb-org-server mongodb-org-shell mongodb-org-mongos mongodb-org-tools


# RQ worker init script
COPY DockerConfigFiles/_init_script_rq_worker_platx /etc/init.d/rqworker

# MongoDB init script
COPY DockerConfigFiles/_init_script_mongodb /etc/init.d/mongodb
RUN chmod 755 /etc/init.d/mongodb

# Clickhouse init script
COPY DockerConfigFiles/_init_script_clickhouse /etc/init.d/clickhouse
RUN chmod 755 /etc/init.d/clickhouse

# Mosquitto init script
COPY DockerConfigFiles/_init_script_mosquitto /etc/init.d/mosquitto
RUN chmod 755 /etc/init.d/mosquitto

# Gunicorn init script
COPY DockerConfigFiles/_init_script_gunicorn /etc/init.d/gunicorn
RUN chmod 755 /etc/init.d/gunicorn

# all_daemons init script
COPY DockerConfigFiles/_init_script_all_daemons /etc/init.d/all_daemons
RUN chmod 755 /etc/init.d/all_daemons


# to enable logging in mylogs files
RUN touch mylogs.log
RUN chmod 777 mylogs.log


# ClickHouse
RUN cd /tmp/
RUN curl https://clickhouse.com/ | sh
RUN ./clickhouse install
RUN sed -i 's/8123/7010/g' /etc/clickhouse-server/config.xml
RUN chown -R root:root /var/lib/clickhouse
COPY DockerConfigFiles/_clickhouse_docker_related_config.xml /etc/clickhouse-server/config.d/docker_related_config.xml


# To keep container alive
CMD /etc/init.d/all_daemons restart;tail -f /dev/null
