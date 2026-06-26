# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

import json
import os
import tempfile
from unittest.mock import ANY, patch

import ossaudit
from ossaudit import audit

from .helpers import PatchedTestCase


class TestScan(PatchedTestCase):
    def _mock_post(self, mock, data_file="vulns01.json"):
        mock.return_value.status_code = 200
        with open(os.path.join("tests", "data", data_file)) as f:
            mock.return_value.json.return_value = json.load(f)

    def test_installed(self) -> None:
        pkgs = [
            audit.packages.Package("requests", "0.10.0"),
            audit.packages.Package("pyyaml", "3.13"),
        ]
        with patch("requests.post") as mock:
            self._mock_post(mock)
            with patch("ossaudit.packages.get_installed", return_value=pkgs):
                vulns = ossaudit.scan(installed=True)
        self.assertEqual(len(vulns), 3)
        self.assertTrue(all(isinstance(v, ossaudit.Vulnerability) for v in vulns))

    def test_from_files(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix="requirements.txt", delete=False
        ) as f:
            f.write("requests==0.10.0\npyyaml==3.13\n")
            tmp_path = f.name
        try:
            with patch("requests.post") as mock:
                self._mock_post(mock)
                vulns = ossaudit.scan(files=[tmp_path])
            self.assertEqual(len(vulns), 3)
        finally:
            os.unlink(tmp_path)

    def test_ignore_by_sonatype_id(self) -> None:
        pkgs = [audit.packages.Package("requests", "0.10.0")]
        with patch("requests.post") as mock:
            self._mock_post(mock)
            with patch("ossaudit.packages.get_installed", return_value=pkgs):
                vulns = ossaudit.scan(
                    installed=True,
                    ignore_ids=["5ec41929-01e3-4daa-b140-a1021b6abf86"],
                )
        self.assertTrue(
            all(v.id != "5ec41929-01e3-4daa-b140-a1021b6abf86" for v in vulns)
        )

    def test_ignore_by_cve(self) -> None:
        pkgs = [audit.packages.Package("requests", "0.10.0")]
        with patch("requests.post") as mock:
            self._mock_post(mock)
            with patch("ossaudit.packages.get_installed", return_value=pkgs):
                vulns = ossaudit.scan(installed=True, ignore_ids=["CVE-2014-1830"])
        self.assertTrue(all(v.cve != "CVE-2014-1830" for v in vulns))

    def test_proxies(self) -> None:
        pkgs = [audit.packages.Package("requests", "0.10.0")]
        proxies = {"https": "http://proxy.example.com:8080"}
        with patch("requests.post") as mock:
            self._mock_post(mock)
            with patch("ossaudit.packages.get_installed", return_value=pkgs):
                ossaudit.scan(installed=True, proxies=proxies)
        self.assertEqual(mock.call_args_list[0][1]["proxies"], proxies)

    def test_audit_error_propagates(self) -> None:
        pkgs = [audit.packages.Package("requests", "0.10.0")]
        with patch("requests.post") as mock:
            mock.return_value.status_code = 401
            with patch("ossaudit.packages.get_installed", return_value=pkgs):
                with self.assertRaises(ossaudit.AuditError):
                    ossaudit.scan(installed=True)

    def test_no_packages(self) -> None:
        with patch("ossaudit.packages.get_installed", return_value=[]):
            vulns = ossaudit.scan(installed=True)
        self.assertEqual(vulns, [])
