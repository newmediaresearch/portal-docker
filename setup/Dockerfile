FROM centos:7

COPY vidispine-api.py /usr/local/bin/vidispine-api
RUN chmod +x /usr/local/bin/vidispine-api

RUN yum install -y postgresql

ENTRYPOINT ["sh", "/quickstart/quickstart.sh"]
