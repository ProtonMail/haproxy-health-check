haproxy-health-check
===============================

version number: 0.0.1
author: Samuele Kaplun

Overview
--------

HAProxy Health Check for EXABGP

Installation / Usage
--------------------

To install use pip:

    $ pip install haproxy-health-check


Or clone the repo:

    $ git clone https://github.com/kaplun/haproxy-health-check.git
    $ python setup.py install
    
Example
-------

Use e.g. inside an EXABGP configuration such as:

    # Check if the service is available to announce a route to
    # it. Since the purpose is high availability, it is expected
    # that another host is present with a similar
    # configuration. IP address for the service is expected to be
    # configured on the loopback interface. You can run the
    # healthcheck process manually to check if it works as
    # expected (-h flag will give you available options)

    process service-haproxy {
        run python -m exabgp healthcheck -s --name haproxy --cmd "haproxy-health-check" --start-ip 0;
        encoder text;
    }

    neighbor 10.0.0.3 {
        description "will announce a route to a service";
        router-id 198.111.227.39;
        local-address 10.0.0.2;
        local-as 65533;
        peer-as 65533;

        api services {
            processes [ service-haproxy ];
        }
    }