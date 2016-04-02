FROM debian:jessie

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3 python3-pip libxml2 libxml2-dev python3-lxml

RUN pip3 install mechanicalsoup py2neo

ADD tmp/run /miner/run
ADD tmp/katrin /miner/katrin
ADD start.sh /miner/

ENTRYPOINT ["/bin/bash", "/miner/start.sh"]