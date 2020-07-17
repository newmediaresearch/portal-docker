Portal in Docker
================

Getting started
---------------
First ensure you have Docker installed: https://hub.docker.com/editions/community/docker-ce-desktop-mac/

You will first need to obtain a Portal License key. You can obtain one from your system integrator.
Once you have it, please rename it
 to `key` and place it inside the root of the repository.

Then execute the following to build the Portal containers:

    make build-3.2.8

To build other versions, simply change the version number after `build-`.
Not all versions of portal are supported yet however, please see the `Makefile` to see which ones have been implemented.

Then execute the following to run:

    make run

This will bring up portal and all containers needed. It may take a while to start, especially on the first run. Once you see "Activiti Online!" then you are normally good to go.

You can now access the portal installation by going to http://127.0.0.1 in your browser.

To shutdown, simply press ctrl-c.
When you want to run again, you do not need to re-build and you can simply do `make run` again.

Configuration
-------------
This .env file will be read by docker-compose and used to configure portal inside the containers. In the sample file, most of the services are assumed to be run as Amazon services, so the actual configuration parameters may vary depending on your specific setup.
