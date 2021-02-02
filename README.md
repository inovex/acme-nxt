ACME-NXT
========

A wrapper around the lego letsencrypt client to generate and
renew a set of certicates.

Usage
-----

    acme-nxt.py [-h] [-c CONFIG] [-l LIMIT] [-v] [-d] {run,renew}

    positional arguments:
      {run,renew}

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            configuration file name (default: mindstorms.ini)
      -l LIMIT, --limit LIMIT
                            section(s) to call lego for
      -v, --verbose
      -d, --dry-run


Examples configurations
-----------------------

DNS backends:
- [designate](designate.ini)
- [rfc2136](bind9.ini)

License
-------

Distributed under the MIT License. See LICENSE for more information.
