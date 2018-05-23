FROM centos:7

ARG VIDISPINE_VERSION

ADD buildimage.sh /
RUN chmod +x /buildimage.sh
RUN VIDISPINE_VERSION=$VIDISPINE_VERSION /buildimage.sh

RUN mkdir /solr-webapp
RUN chown vidispine:vidispine /solr-webapp

COPY docker-entrypoint.sh /usr/local/bin/
VOLUME /var/lib/vidispine/solr/collection1/data

ENTRYPOINT ["sh", "docker-entrypoint.sh"]

EXPOSE 8983
