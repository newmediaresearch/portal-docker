Portal in Docker
================


Getting started
---------------

You will first need to obtain a Portal License key. You can obtain one from your system integrator.
Once you have it, please rename it to `key` and place it inside the `portal` directory.

Then execute the following:

    make run-3.2.8

This will bring up portal 3.2.8 and all containers needed. To bring up other versions, simply change the version number after `run-`.

Not all versions of portal are supported yet however, please see the `Makefile` to see which ones have been implemented.

You can now access the portal installation by going to http://your.docker.server in your browser.

To shutdown, simply press ctrl-c.

Configuration
-------------

This .env file will be read by docker-compose and used to configure
portal inside the containers. In the sample file, most of the services
are assumed to be run as Amazon services, so the actual configuration
parameters may vary depending on your specific setup.
