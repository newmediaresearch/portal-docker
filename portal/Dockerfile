FROM centos:7

ARG PORTAL_DOWNLOAD_URL

ENV LANG en_US.utf8
ENV LC_ALL en_US.UTF-8

RUN yum install -y curl nmap-ncat which

WORKDIR /install
RUN curl $PORTAL_DOWNLOAD_URL -o Portal.tar
RUN tar xvf Portal.tar
RUN yum install -y RedHat*[0-9]/resources/portal/*.rpm RedHat*[0-9]/resources/portal/postgresql/*.rpm

WORKDIR /
RUN rm -rf /install/RedHat* /install/Portal.tar
RUN yum clean all

RUN echo "COMPRESS_ENABLED = False" >> /opt/cantemo/portal/portal/localsettings.py
RUN echo "STATSD_CELERY_SIGNALS = True" >> /opt/cantemo/portal/portal/localsettings.py

ADD docker-entrypoint.sh /
ADD logging.conf /etc/cantemo/portal/logging.conf
ADD nginx/pass_access_scheme.conf /etc/nginx/conf.d/pass_access_scheme.conf

# Make sure the logs are written to stdout in the container
RUN rm /var/log/nginx/access.log /var/log/nginx/error.log
RUN ln -s /dev/stdout /var/log/nginx/access.log
RUN ln -s /dev/stderr /var/log/nginx/error.log
RUN rm /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/example_ssl.conf

# There are too many layers of proxies between portal and the
# TLS-endpoint that the https header gets lost
RUN sed -i -e 's,X-Scheme.*,X-Scheme $pass_access_scheme;,' /etc/nginx/conf.d/portal.conf

RUN mkdir -p /startup.d/
RUN mkdir -p /setup.d/
RUN mkdir -p /setup-post-wizard.d/

RUN localedef --quiet -c -i en_US -f UTF-8 en_US.UTF-8

ADD key /etc/cantemo/portal/key

WORKDIR /opt/cantemo/portal

ENTRYPOINT ["/docker-entrypoint.sh"]
