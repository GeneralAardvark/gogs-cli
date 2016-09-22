#!/usr/bin/env python

import requests
import argparse
try:
    from configparser import ConfigParser
except:
    from ConfigParser import ConfigParser
import sys
import os
import re
from requests.exceptions import ConnectTimeout, ConnectionError

cfg = ConfigParser()
cfg_file = os.path.join(os.path.expanduser("~"), '.config', 'gogs.cfg')
s = requests.Session()


def choose_schema(gogs_host):
    global api
    for schema in ("https://", "http://"):
        try:
            api = "{}{}/api/v1/".format(schema, gogs_host)
            r = call_api('user/', True)
            if not r.status_code:
                continue
            else:
                return r
        except ConnectTimeout:
            continue
        except ConnectionError:
            break
    sys.exit("Error connecting to {}.".format(gogs_host))

def read_config():
    cfg = ConfigParser()
    cfg_file = os.path.join(os.path.expanduser("~"), '.config', 'gogs.cfg')
    if cfg.read(cfg_file):
        c = []
        for e in ('gogs_host', 'token', 'username'):
            try:
                c.append(cfg.get('gogs', e))
            except:
                sys.exit("'{}' missing or incorrectly formatted in {}.".format(e, cfg_file))
        return c
    else:
        sys.exit("{} not found or incorrectly formatted.".format(cfg_file))


def validate_config(c):
    global username
    gogs_host, token, username = c
    s.headers = {'Authorization': 'token {}'.format(token)}
    r = choose_schema(gogs_host)
    if r.status_code == 404:
        sys.exit("Does username {}, exist?".format(username))
    if r.status_code == 403:
        sys.exit("Unable to authenticate with token specified.")
    if r.status_code != 200:
        sys.exit("Got a {} when connecting to {}.".format(r.status_code, gogs_user))
    if r.json()['username'] != username:
        sys.exit("Token and username, {}, do not match.".format(username))


def call_api(command, test=False):
    r = s.get(api + command, timeout=1)
    if test:
        return r
    if r.status_code == 200:
        return r.json()
    # Code to get around 500 error when getting branches for empty repos.
    if r.status_code == 500 and "branches" in command:
        return []
    # End.
    sys.exit("{} when calling {}.".format(r.status_code, command))


class colour:
    red = '\033[1;31m'
    green = '\033[1;32m'
    yellow = '\033[1;33m'
    end = '\033[1;m'


def main():
    parser = argparse.ArgumentParser(description="Dirty Gogs Repo Searcher")
    options = parser.add_mutually_exclusive_group()
    options.add_argument('-clone', help="git clone commands.", action="store_true")
    output_opts = options.add_argument_group()
    output_opts.add_argument('-ssh', help="Show git ssh url", action="store_true")
    branches = options.add_mutually_exclusive_group()
    branches.add_argument('-branches', help="Show branches.", action="store_true")
    branches.add_argument('-mybranches', help="Show my branches.", action="store_true")
    parser.add_argument('search', nargs="?", help="Search term for repo.", default=".")
    args = parser.parse_args()

    validate_config(read_config())

    repos = call_api('user/repos')

    if len(repos) == 0:
        sys.exit('Error, no repos to list')

    searchterm = re.compile(args.search, re.I)

    for repo in repos:
        if searchterm.search(repo['full_name']):
            if args.clone:
                print("git clone {}".format(repo['ssh_url']))
                continue
            output = repo['full_name']
            output += " {}{}{}".format(colour.red, repo['html_url'], colour.end)
            if args.ssh:
                output += " {}{}{}".format(colour.green, repo['ssh_url'], colour.end)
            if args.branches or args.mybranches:
                branches = call_api('repos/{}/branches'.format(repo['full_name']))
                for branch in branches:
                    if args.mybranches:
                        if branch['commit']['author']['username'] != username:
                            continue
                    print(output)
                    print("\t{}{} {}{}{}".format(
                        colour.green,
                        branch['commit']['author']['username'],
                        colour.yellow,
                        branch['name'],
                        colour.end))
            else:
                print(output)


if __name__ == '__main__':
    main()
