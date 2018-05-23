FROM centos:7

ARG VIDISPINE_VERSION

ADD buildimage.sh /
RUN chmod +x /buildimage.sh
RUN VIDISPINE_VERSION=$VIDISPINE_VERSION /buildimage.sh

COPY docker-entrypoint.sh /usr/local/bin/

WORKDIR /opt/vidispine/transcoder/

USER vidispine
ENTRYPOINT ["sh", "docker-entrypoint.sh"]

EXPOSE 8888
