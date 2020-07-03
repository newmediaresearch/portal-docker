FROM centos:7

ARG VIDISPINE_VERSION

ADD buildimage.sh /
ADD key /usr/local/bin/key
RUN chmod +x /buildimage.sh
RUN VIDISPINE_VERSION=$VIDISPINE_VERSION /buildimage.sh

RUN yum install -y PyYAML
COPY vidispine_server_config.py /usr/local/bin/
COPY vidispine_license_extractor.py /usr/local/bin/
RUN python /usr/local/bin/vidispine_server_config.py
RUN python /usr/local/bin/vidispine_license_extractor.py

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

USER vidispine
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 8080
