
# ossaudit-ng (Next Generation)

[![CI](https://github.com/stuartz/ossaudit/actions/workflows/ci.yml/badge.svg)](https://github.com/stuartz/ossaudit/actions/workflows/ci.yml)
![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

A fork of https://github.com/illikainen/ossaudit.git which appears to be no longer maintained.

This fork includes protions of PRs by sseide on the original ossaudit.git

## New Features
  - Added JSON output, config file support, Bearer token auth, HTTP/HTTPS proxy support, and ability to import.
  - Works with the new API URL: "https://api.guide.sonatype.com/api/v3/"

See [HISTORY.md][4] for the full changelog.

## About

`ossaudit` uses [Sonatype OSS Index][1] to audit Python packages for
known vulnerabilities.

It can check installed packages and/or packages specified in dependency
files.  The following formats are supported with [dparse][2]:

- PIP requirement files
- Pipfile
- Pipfile.lock
- tox.ini
- conda.yml


## Installation

### From PyPI

```sh
pip install ossaudit-ng
```

### From source (development)

```sh
pip install -e .[dev]
```


## Usage

```sh
$ ossaudit --help
Usage: ossaudit [OPTIONS]

Options:
  -c, --config TEXT    Configuration file.
  -i, --installed      Audit installed packages.
  -f, --file FILENAME  Audit packages in file (can be specified multiple
                       times).
  --token TEXT         Token for authentication.
  --column TEXT        Column to show; repeatable or comma-separated.
                       Available: name, version, id, cve, cvss_score, title,
                       description.  [default: name, version, title]
  --ignore-id TEXT     Ignore a vulnerability by Sonatype ID or CVE (can be
                       specified multiple times).
  --ignore-cache       Temporarily ignore existing cache.
  --reset-cache        Remove existing cache.
  --json               Output vulnerabilities as json list
  --json-full          Output all dependencies found and their vulnerabilities
                       as json list (columns given are ignored)
  --http-proxy TEXT    HTTP proxy URL.
  --https-proxy TEXT   HTTPS proxy URL.
  --help               Show this message and exit.
```

## Exit codes

The command exits with a distinct status so it can be used as a CI gate
that tells "found something" apart from "could not run":

| Code | Meaning                                                        |
|------|----------------------------------------------------------------|
| `0`  | Ran successfully; no vulnerabilities found.                    |
| `1`  | Ran successfully; one or more vulnerabilities found.           |
| `2`  | Could not run (bad configuration, invalid credentials, rate limiting, or a usage error). |

## As import

`scan()` accepts these optional arguments:

- `installed=True` — audit installed packages
- `files=["path/requirements.txt"]` — requirements/lock files to audit (a list)
- `token="..."` — OSS Index API token
- `ignore_ids=["CVE-..."]` — vulnerability IDs or CVEs to skip (a list)
- `ignore_cache=True` — bypass the local cache
- `proxies={"https": "http://proxy:8080", "http": "http://proxy:8080"}`

```python
from ossaudit import scan
list_of_vulnerabilites = scan(installed=True)  # Pass options as args
for v in list_of_vulnerabilites:
  # v is type <class 'ossaudit.audit.Vulnerability'>
  print(v.name, v.version, v.title, v.cvss_score)
```

## Configuration

[Appdirs][3] is used to determine storage paths.  This means that the
location of the configuration file is platform-specific:

- `*nix`: `~/.config/ossaudit/config.ini`
- `macOS`: `~/Library/Preferences/ossaudit/config.ini`
- `Windows`: `C:\Users\<username>\AppData\Local\ossaudit\ossaudit\config.ini`

It can be overridden with the `--config` command-line argument and with
the `OSSAUDIT_CONFIG` environment variable.

Example configuration:

```ini
[ossaudit]
# Optional: OSS Index API token (Bearer token auth).
# A free account and token can be created at https://ossindex.sonatype.org/
#token = string

# Optional: comma-separated list of columns to show.
# Default: name, version, title
# Supported: id, name, version, cve, cvss_score, title, description
#columns = name,version,title,cvss_score

# Optional: comma-separated list of vulnerability IDs (Sonatype ID or CVE) to ignore.
#ignore_ids = x,y,z

# Optional: Ignore cache
#ignore_cache = True

# Optional: Reset the cache
#reset_cache = True

# Optional: Output format to json
#json = True

# Optional: Full output of OSS Index results to json
#json_full = True

# Optional: HTTP/HTTPS proxy (can also be set via HTTP_PROXY/HTTPS_PROXY env vars)
#http_proxy = http://proxy.example.com:8080
#https_proxy = http://proxy.example.com:8080
```

Authentication is **not** required.  However, requests are rate limited
and authenticated requests are less restricted.  A free account and API
token can be created on [OSS Index][1].


[1]: https://ossindex.sonatype.org/
[2]: https://github.com/pyupio/dparse
[3]: https://github.com/ActiveState/appdirs
[4]: https://github.com/stuartz/ossaudit/blob/master/HISTORY.md
