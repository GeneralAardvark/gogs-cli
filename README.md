# gogs-cli
CLI to list GOGS repositories and branches

## Config File
Requires a suitably formatted configuration file.

Generate a token via `Your Settings` > `Applications` > `Generate New Token`

### ~/.config/gogs.cfg

```
[gogs]
gogs_host: <gogs hostname>
token: <user generated token>
username: <username>
```

## Command line options

```
usage: gogs [-h] [-clone] [-ssh] [-branches | -mybranches] [--user USER] [search]

Dirty Gogs Repo Searcher

positional arguments:
  search      Search term for repo.

optional arguments:
  -h, --help   show this help message and exit
  -clone       git clone commands.
  -branch      Show branches.
  -mybranch    Show my branches.
  --user USER  Find -branches owned by specified user.
```

## Example Usage

List all repos `gogs`

Search for repositories `gogs <search>`

Git clone repositories locally. `gogs <search> -clone | bash`

Find branches currently owned by me (last commited) `gogs [<search>] -mybranches`

Find branches owned by other people `gogs [<search>] -branches --user
<someone>`

