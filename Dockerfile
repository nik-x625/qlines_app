FROM debian:buster
ENV TZ Europe/Berlin
RUN apt-get update -y
RUN apt-get -y install ntp ssh vim net-tools python3 python3-pip wget tzdata git apache2 tcpdump
RUN apt-get -y install redis
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN apt-get -y install libapache2-mod-wsgi-py3
RUN dpkg-reconfigure -f noninteractive tzdata
RUN pip3 install flask flask_login redis rq pymongo
RUN useradd flask


# bashrc content
ADD bashrc_append /tmp/
RUN cat /tmp/bashrc_append >> /root/.bashrc


# apache config
ADD apache_configuration.conf /tmp/
RUN cp /tmp/apache_configuration.conf /etc/apache2/sites-available/000-default.conf
RUN echo "ServerName 127.0.0.1" >> /etc/apache2/apache2.conf
RUN a2enmod rewrite
RUN sed -i 's/Listen 80/Listen 8080/g' /etc/apache2/ports.conf
RUN /etc/init.d/apache2 restart

CMD tail -f /dev/null

# git
git config --global user.email "Mehdi's email from docker"
git config --global user.name "Mehdi from docker"
