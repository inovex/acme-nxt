#!/usr/bin/env python3
'''
A wrapper around the lego letsencrypt client to generate and
renew a set of certicates.

Example configuration file:

"""
### designate.ini
[DEFAULT]
# Letsencrypt account (required)
Email = user@example.com

# ACME API endpoint (required)
Server = https://acme-staging-v02.api.letsencrypt.org/directory
# Productiv API
# Server = https://acme-v02.api.letsencrypt.org/directory

# DNS backend to use
DNS = designate

# Environment variables can be set by Env_ prefix
Env_OS_CLOUD = user-acme

# Arguments for the run method of lego prefixed by Run_
Run_Run-Hook = echo done

# Arguments for the renew method of lego prefixed by Run_
Renew_Days = 30
Renew_Renew-Hook = echo renew
# Flags without values should be defined without a value
# Renew_No-Bundle =

# Every global parameter can be overridden or set in each section
[c.example.com]
# Subject alt names (cn is derived from first entry)
Domains = c.example.com, service.example.com
# Enable tls challenge by defining the var
TLS =

[d.example.com]
Domains = d.example.com, service.example.com

[e.example.com]
Domains = *.example.com
"""

'''

import argparse
import configparser
import os
from typing import Dict

from sh import lego, ErrorReturnCode  # pylint: disable=no-name-in-module

GLOBAL_ARGS = (
    'csr', 'kid', 'hmac', 'key-type', 'filename', 'path',
    'http.port', 'http.proxy-header', 'http.webroot', 'http.memcached-host',
    'tls.port', 'dns', 'dns.resolvers', 'http-timeout', 'dns-timeout',
    'cert.timeout',
)
GLOBAL_FLAGS = ('eab', 'http', 'tls', 'dns.disable-cp', 'pem', )


def lego_cmd(cmd: str, params: Dict,
             verbose: bool = False, dry_run: bool = False):
    """command wrapper for lego."""
    params['env'] = {}
    args = []

    # required args
    global_args = ['--accept-tos', '--server', params['server'],
                   '--email', params['email']]

    for arg, val in params.items():
        if arg == 'domains':
            params[arg] = [d.strip() for d in val.split(",")]
            continue
        if arg.startswith("env_"):
            params['env'][arg[4:].upper()] = val
            continue
        if cmd in ('run', 'renew') and arg.startswith(f'{cmd}_'):
            args.append(f'--{arg[len(cmd) + 1:]}')
            if val:
                args.append(val)
            continue
        if arg in GLOBAL_ARGS:
            global_args.extend([f'--{arg}', val])
            continue
        if arg in GLOBAL_FLAGS:
            global_args.append(f'--{arg}')

    for dom in params['domains']:
        global_args.extend(['--domains', dom])

    os.environ.update(params['env'])

    if verbose or dry_run:
        print(f'Section: {params["section"]}')
        print(f'Environment: {params["env"]}')
        print('lego', ' '.join(global_args), cmd, ' '.join(args))
        print()

    if not dry_run:
        try:
            lego(global_args, cmd, args)
        except ErrorReturnCode as exc:
            print(exc.stdout)
            raise exc


def main():
    """main."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-c', '--config',
        default='mindstorms.ini',
        help='configuration file name (default: mindstorms.ini)')
    parser.add_argument(
        '-l', '--limit', action='append',
        help='section(s) to call lego for')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('command', choices=('run', 'renew'))
    args = parser.parse_args()

    cfg = configparser.ConfigParser()
    cfg.read(args.config)

    for section in cfg.sections():
        if args.limit and section not in args.limit:
            continue
        params = dict(cfg[section])
        params['section'] = section
        lego_cmd(args.command, params, args.verbose, args.dry_run)


if __name__ == "__main__":
    main()
