FROM debian:buster
RUN apt-get update
RUN apt-get -y install ntp ssh vim tcpdump tcpflow net-tools python3 python3-pip lsb-release git firefox-esr curl apache2 libapache2-mod-wsgi
RUN apt-get install dirmngr gnupg apt-transport-https software-properties-common ca-certificates 
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN pip3 install selenium numpy pandas bs4 pymongo flask flask_login
CMD tail -f /dev/null
