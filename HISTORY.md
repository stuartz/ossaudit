# History

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
