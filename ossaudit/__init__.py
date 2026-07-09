# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

__version__ = "1.0.1"
__project__ = "ossaudit-ng"

from typing import Dict, List, Optional

from .audit import AuditError, Vulnerability, components, flatten_vuln_list
from . import packages as _packages

__all__ = ["AuditError", "Vulnerability", "scan"]


def scan(
        installed: bool = False,
        files: Optional[List[str]] = None,
        token: Optional[str] = None,
        ignore_ids: Optional[List[str]] = None,
        ignore_cache: bool = False,
        proxies: Optional[Dict[str, str]] = None,
) -> List[Vulnerability]:
    """Audit packages and return a list of vulnerabilities.

    Parameters
    ----------
    installed:
        Audit currently installed packages.
    files:
        Paths to requirements files to audit.
    token:
        Sonatype OSS Index API token.
    ignore_ids:
        Sonatype IDs or CVE IDs to exclude from results.
    ignore_cache:
        Skip the local cache and always query the API.
    proxies:
        Proxy URLs keyed by scheme, e.g. ``{"https": "http://proxy:8080"}``.

    Returns
    -------
    List[Vulnerability]
        Every vulnerability found, minus any in *ignore_ids*.

    Raises
    ------
    AuditError
        On API authentication, rate-limit, or unexpected status errors.
    """
    pkgs = []  # type: list
    if installed:
        pkgs += _packages.get_installed()
    if files:
        handles = [open(f, encoding="utf-8") for f in files]
        try:
            pkgs += _packages.get_from_files(handles)
        finally:
            for h in handles:
                h.close()

    all_coordinates = components(pkgs, token, proxies, ignore_cache)
    vulns = flatten_vuln_list(all_coordinates)

    if ignore_ids:
        vulns = [
            v for v in vulns
            if v.id not in ignore_ids and v.cve not in ignore_ids
        ]

    return vulns
