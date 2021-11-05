FROM debian:buster
ENV TZ Europe/Berlin
RUN apt-get update -y
RUN apt-get -y install ntp ssh vim net-tools python3 python3-pip wget tzdata git apache2 libapache2-mod-wsgi tcpdump
RUN apt-get -y install redis
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN dpkg-reconfigure -f noninteractive tzdata
RUN pip3 install flask flask_login redis rq pymongo


# bashrc content
ADD bashrc_append /tmp/
RUN cat /tmp/bashrc_append >> /root/.bashrc


# apache config
ADD apache_configuration.conf /tmp/
RUN cp /tmp/apache_configuration.conf /etc/apache2/sites-available/000-default.conf
RUN echo "ServerName 127.0.0.1" >> /etc/apache2/apache2.conf
RUN a2enmod rewrite
RUN useradd flask
RUN /etc/init.d/apache2 start

CMD tail -f /dev/null
