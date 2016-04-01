FROM debian:jessie

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3 python3-pip

RUN pip3 install mechanicalsoup py2neo

ADD ../../run /
ADD ../../katrin /
ADD start.sh /

ENTRYPOINT ["/bin/bash", "/start.sh"]