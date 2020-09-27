FROM ubuntu:18.04

COPY start.sh /start.sh

RUN apt-get update \
    && apt-get -y install curl \
    && curl https://s3.us-west-2.amazonaws.com/amazon-ssm-us-west-2/latest/debian_amd64/amazon-ssm-agent.deb -o /tmp/amazon-ssm-agent.deb \
    && dpkg -i /tmp/amazon-ssm-agent.deb \
    && cp /etc/amazon/ssm/seelog.xml.template /etc/amazon/ssm/seelog.xml

CMD ["bash", "start.sh"]
