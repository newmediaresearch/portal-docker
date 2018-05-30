Portal in Docker
================

A license key for Portal is required. You can obtain one from your system integrator.

Building
--------

> docker-compose build \
--build-arg VIDISPINE_VERSION=4.12 \
--build-arg PORTAL_DOWNLOAD_URL=http://www2.cantemo.com/files/transfer/07/07382da5cd68561ee1035274871ea28e0d64e045/RedHat7_Portal_3.4.1.tar

Configuration
-------------

This .env file will be read by docker-compose and used to configure
portal inside the containers. In the sample file, most of the services
are assumed to be run as Amazon services, so the actual configuration
parameters may vary depending on your specific setup.

Running
-------

Once you have configured the docker-compose environment you can bring up the system with the commands:

> docker-compose up -d

This will bring up all the portal components and you can now access
the portal installation by going to http://your.docker.server in your browser.
