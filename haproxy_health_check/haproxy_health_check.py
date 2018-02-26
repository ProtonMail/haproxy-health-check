# -*- coding: utf-8 -*-
"""
This simple script verifies that: 
 * the local HAProxy is reachable through the provided socket
 * that all backends (or the specified ones) are UP
 * that all frontends (or the specified ones) are OPEN
""" 

from __future__ import print_function


import sys
import argparse

from haproxyadmin.haproxy import HAProxy


def get_options():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-s', '--socket', 
        help="Path to HAProxy stats socket (default to %(default)s)", 
        default="/var/lib/haproxy/stats", 
    )
    parser.add_argument(
        '-b', '--backend',
        dest='backends',
        help="Name of backend that must be UP (default to all)",
        action='append',
        metavar='BACKEND',
    )
    parser.add_argument(
        '-f', '--frontend',
        dest='frontends',
        help="Name of frontend that must be OPEN (default to all)",
        action='append',
        metavar='FRONTEND',
    )
    return parser.parse_args()


def check(haproxy, options):
    for backend in haproxy.backends():
        if not options.backends or backend.name in options.backends:
            if backend.status != 'UP':
                raise Exception("Backend %s is in status %s" % (backend.name, backend.status))
    for frontend in haproxy.frontends():
        if not options.frontends or frontend.name in options.frontends:
            if frontend.status != 'OPEN':
                raise Exception("Frontend %s is in status %s" % (frontend.name, frontend.status))


def main():
    try:
        options = get_options()
        haproxy = HAProxy(socket_file=options.socket)
        check(haproxy, options)
    except Exception as err:
        print("HAProxy check failed: %s" % err, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()