# History

## 2.0.0

### Breaking / behavior changes

- Exit codes are now distinct so a CI gate can tell "found something"
  from "could not run": `0` no vulnerabilities, `1` vulnerabilities
  found, `2` the audit could not run (bad configuration, invalid
  credentials, rate limiting, or a usage error). Previously operational
  errors surfaced as `1` (indistinguishable from findings), and
  `--json-full` exited with the vulnerable-package *count*, which wrapped
  to `0` at 256 packages.
- Command-line options now take precedence over the configuration file.
  Previously a config value silently overrode an explicit CLI flag.
- The configuration section and environment-variable prefix are resolved
  from the stable app name (`[ossaudit]` / `OSSAUDIT_*`), and config keys
  may be written with either hyphens or underscores. This restores the
  documented behavior that the 1.0.0 rebrand broke.
- `python_requires` is now `>=3.8` (was `>=3.5`).

### Fixes

- Cached vulnerability data now expires after `CACHE_TIME`; the freshness
  check was inverted, so cache entries never expired.
- A clean audit prints a summary again instead of nothing, and `--json`
  always emits a valid (possibly empty) array.
- `--json-full` no longer crashes when combined with `--ignore-cache`.
- Versions are recovered from `refs/tags/` direct references even when
  the tag looks like a commit hash (e.g. a date tag like `20240101`).
- `--column` names are matched case-insensitively in JSON output,
  matching the table output.
- `_Version` no longer relies on a private `packaging` API that newer
  `packaging` releases have deprecated and will remove.

### Project

- Dev tools are declared via `extras_require["dev"]`
  (`pip install -e '.[dev]'`).
- Added a GitHub Actions CI matrix (Python 3.8–3.14) with a 100%
  coverage gate, a security policy, and Dependabot configuration;
  classifiers updated through 3.14.

## 1.0.3

- Fix packages referenced via a PEP 508 direct reference (e.g.
  `pkg @ file:///path/to/pkg-1.2.3-py3-none-any.whl`) being silently
  audited as version `0` instead of the real version. The version is
  now recovered from wheel and sdist (`.tar.gz`/`.zip`) filenames, and
  from VCS refs (e.g. `pkg @ git+https://.../pkg.git@v1.2.3`) when the
  ref looks like a version tag rather than a branch or commit hash.

## 1.0.2

- Fix the default configuration file not being found. The `1.0.0`
  rebrand changed the config/cache directory name, which broke the
  default `~/.config/ossaudit/config.ini` lookup on existing installs
  until `--config` was passed explicitly.

## 1.0.1

- Read `__version__`/`__project__` from source in `setup.py` to avoid
  an import error during build.
- README and PyPI long description updates.

## 1.0.0 (rebrand to `ossaudit-ng`)

- Forked and rebranded as `ossaudit-ng` since the upstream project
  appears unmaintained.
- Add support for the new Sonatype OSS Index v3 API.
- Add Bearer token authentication.
- Add `--json`/`--json-full` output.
- Add HTTP/HTTPS proxy support.
- Add a programmatic API (`ossaudit.scan()`).
- Add `--reset-cache` to delete cached vulnerability data.
- Add `--ignore-cache` to temporarily ignore cached vulnerability data.
- Handle invalid JSON caches (by ignoring/overwriting them).
- Allow to ignore vulnerabilities by Sonatype ID or CVE ID.
- Properly handle the configuration file.

## 0.5.0

- Skip duplicate packages in the requirement files.


## 0.4.0

- Add support for ignoring vulnerabilities by ID.
- Expose all configuration options as command-line arguments.
- Change `--config-file` to `--config`.
- Show all columns as text to avoid inaccurate formatting of certain
  version numbers.
- Always print a summary that shows the number of audited packages.


## 0.3.0

- Add support for customized columns.
- Add help strings for `--help`.
- Exit with non-zero status code if any vulnerabilities are found.


## 0.2.0

- Add support for authenticated requests.
- Use platform-specific storage paths.
- Fix bug that caused invalid cache misses.

## 0.1.0

- Initial release.
