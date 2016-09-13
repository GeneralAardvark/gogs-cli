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
usage: gogs [-h] [-clone] [-url] [-ssh] [-branches | -mybranches] [search]

Dirty Gogs Repo Searcher

positional arguments:
  search      Search term for repo.

optional arguments:
  -h, --help  show this help message and exit
  -clone      git clone commands.
  -branch     Show branches.
  -mybranch   Show my branches.
```

## Example Usage

List all repos `gogs`

Search for repositories `gogs <search>`

Display URL to repositories `gogs <search> -url`

Git clone repositories locally. `gogs <search> -clone | bash`

Find branches currently owned by me (last commited) `gogs <search> -mybranches`
