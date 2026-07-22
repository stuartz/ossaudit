# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

import json
import tempfile
from functools import partial
from pathlib import Path
from unittest.mock import ANY, patch

from click.testing import CliRunner

from ossaudit import audit, cli, const, packages

from .helpers import PatchedTestCase

Vulnerability = partial(
    audit.Vulnerability,
    **{f: f
       for f in audit.Vulnerability._fields},
)


class TestCli(PatchedTestCase):
    def test_run(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        self.assertEqual(result.exit_code, 0)

    def test_installed(self) -> None:
        runner = CliRunner()

        pkgs = [
            packages.Package("a", "1.1"),
            packages.Package("b", "2.2"),
        ]

        with patch("ossaudit.packages.get_installed") as get_installed:
            get_installed.return_value = pkgs
            with patch("ossaudit.audit.components") as components:
                components.return_value = []
                result = runner.invoke(cli.cli, ["--installed"])
                self.assertEqual(result.exit_code, 0)
                components.assert_called_with(pkgs, None, None, False)

    def test_files(self) -> None:
        runner = CliRunner()

        pkgs = [
            packages.Package("a", "1.1"),
            packages.Package("b", "2.2"),
        ]

        with patch("ossaudit.packages.get_from_files") as get_from_files:
            get_from_files.return_value = pkgs
            with patch("ossaudit.audit.components") as components:
                components.return_value = []
                with tempfile.NamedTemporaryFile() as tmp:
                    result = runner.invoke(cli.cli, ["--file", tmp.name])
                    self.assertEqual(result.exit_code, 0)
                    components.assert_called_with(pkgs, None, None, False)

    def test_proxies(self) -> None:
        with patch("ossaudit.packages.get_installed") as get_installed:
            get_installed.return_value = [packages.Package("a", "1.1")]
            with patch("ossaudit.audit.components") as components:
                components.return_value = []
                runner = CliRunner()
                result = runner.invoke(cli.cli, [
                    "--installed",
                    "--http-proxy", "http://proxy:8080",
                    "--https-proxy", "http://proxy:8443",
                ])
                self.assertEqual(result.exit_code, 0)
                components.assert_called_with(
                    ANY,
                    None,
                    {"http": "http://proxy:8080", "https": "http://proxy:8443"},
                    False,
                )

    def test_mixed(self) -> None:
        runner = CliRunner()

        files = [
            packages.Package("c", "1.1"),
            packages.Package("d", "2.2"),
        ]

        installed = [
            packages.Package("a", "1.1"),
            packages.Package("b", "2.2"),
        ]

        with patch("ossaudit.packages.get_from_files") as get_from_files:
            get_from_files.return_value = files
            with patch("ossaudit.packages.get_installed") as get_installed:
                get_installed.return_value = installed

                with patch("ossaudit.audit.components") as components:
                    components.return_value = []
                    with tempfile.NamedTemporaryFile() as tmp:
                        result = runner.invoke(
                            cli.cli, ["--installed", "--file", tmp.name]
                        )
                        self.assertEqual(result.exit_code, 0)
                        components.assert_called_with(
                            installed + files,
                            None,
                            None,
                            False,
                        )

    def test_credentials(self) -> None:
        with const.CONFIG.open("w") as f:
            f.write("[{}]\n token=xyz".format(const.APP_NAME))

        runner = CliRunner()
        with patch("ossaudit.packages.get_installed") as get_installed:
            get_installed.return_value = [packages.Package("a", "1.1")]
            with patch("ossaudit.audit.components") as components:
                components.return_value = []
                result = runner.invoke(cli.cli, ["--installed"])
                self.assertEqual(result.exit_code, 0)
                components.assert_called_with(ANY, "xyz", None, False)

    def test_audit_error(self) -> None:
        with patch("ossaudit.packages.get_installed") as get_installed:
            get_installed.return_value = []
            with patch("ossaudit.audit.components") as components:
                components.side_effect = audit.AuditError("xyz")
                runner = CliRunner()
                result = runner.invoke(cli.cli, ["--installed"])
                self.assertTrue("xyz" in result.output)
                # 2 == could not run (distinct from 1 == vulns found).
                self.assertEqual(result.exit_code, 2)

    def test_config_error(self) -> None:
        with const.CONFIG.open("w") as f:
            f.write("...")

        runner = CliRunner()
        result = runner.invoke(cli.cli)
        self.assertEqual(result.exit_code, 2)

    def test_have_vulnerabilities(self) -> None:
        with patch("ossaudit.packages.get_installed"):
            with patch("ossaudit.audit.components") as components:
                components.return_value = []
                with patch("ossaudit.audit.flatten_vuln_list") as flatten:
                    flatten.return_value = [Vulnerability()]
                    runner = CliRunner()
                    result = runner.invoke(cli.cli, ["--installed"])
                    # 1 == vulnerabilities found (distinct from 2 == error).
                    self.assertEqual(result.exit_code, 1)
                    self.assertTrue("1 vulnerabilities" in result.output)

    def test_json_column_case_insensitive(self) -> None:
        # A capitalized-but-valid column must resolve in --json output
        # (matching the table path), keeping the caller's spelling as
        # the key. Vulnerability() sets each field to its own name.
        with patch("ossaudit.packages.get_installed"):
            with patch("ossaudit.audit.components") as components:
                components.return_value = []
                with patch("ossaudit.audit.flatten_vuln_list") as flatten:
                    flatten.return_value = [Vulnerability()]
                    runner = CliRunner()
                    result = runner.invoke(
                        cli.cli,
                        ["--installed", "--json", "--column", "Name",
                         "--column", "CVE"],
                    )
                    self.assertEqual(
                        json.loads(result.output),
                        [{"Name": "name", "CVE": "cve"}],
                    )

    def test_no_vulnerabilities(self) -> None:
        with patch("ossaudit.packages.get_installed"):
            with patch("ossaudit.audit.components") as components:
                components.return_value = []
                runner = CliRunner()
                result = runner.invoke(cli.cli, ["--installed"])
                self.assertEqual(result.exit_code, 0)
                # A clean audit must still print a summary, not be silent.
                self.assertTrue("0 vulnerabilities" in result.output)

    def test_no_vulnerabilities_json(self) -> None:
        with patch("ossaudit.packages.get_installed"):
            with patch("ossaudit.audit.components") as components:
                components.return_value = []
                runner = CliRunner()
                result = runner.invoke(cli.cli, ["--installed", "--json"])
                self.assertEqual(result.exit_code, 0)
                # --json must always emit a valid (possibly empty) array.
                self.assertEqual(json.loads(result.output), [])

    def test_ignore_some_ids_arg(self) -> None:
        vulns = [
            Vulnerability(id="0"),
            Vulnerability(id="1"),
            Vulnerability(id="2"),
            Vulnerability(id="10", cve="CVE-10"),
            Vulnerability(id="20", cve="CVE-20"),
            Vulnerability(id="30", cve="CVE-30"),
            Vulnerability(id="31", cve="CVE-31"),
            Vulnerability(cve="CVE-32"),
        ]

        with patch("ossaudit.packages.get_installed"):
            with patch("ossaudit.audit.components") as components:
                components.return_value = []
                with patch("ossaudit.audit.flatten_vuln_list") as flatten:
                    flatten.return_value = vulns
                    runner = CliRunner()
                    args = [
                        "--installed", "--ignore-id", "1", "--ignore-id", "20",
                        "--ignore-id", "CVE-30"
                    ]
                    result = runner.invoke(cli.cli, args)
                    self.assertNotEqual(result.exit_code, 0)
                    self.assertTrue("5 vulnerabilities" in result.output)

    def test_ignore_all_ids_arg(self) -> None:
        vulns = [
            Vulnerability(id="0"),
            Vulnerability(id="1"),
            Vulnerability(id="2", cve="CVE-2"),
            Vulnerability(id="3", cve="CVE-3"),
            Vulnerability(cve="CVE-4")
        ]

        with patch("ossaudit.packages.get_installed"):
            with patch("ossaudit.audit.components") as components:
                components.return_value = []
                with patch("ossaudit.audit.flatten_vuln_list") as flatten:
                    flatten.return_value = vulns
                    runner = CliRunner()
                    args = [
                        "--installed", "--ignore-id", "0", "--ignore-id", "1",
                        "--ignore-id", "2", "--ignore-id", "CVE-3",
                        "--ignore-id", "CVE-4"
                    ]
                    result = runner.invoke(cli.cli, args)
                    self.assertEqual(result.exit_code, 0)

    def test_reset_cache(self) -> None:
        cache = Path(tempfile.NamedTemporaryFile(delete=False).name)

        self.assertTrue(cache.exists())
        with patch("ossaudit.const.CACHE", cache):
            runner = CliRunner()
            result = runner.invoke(cli.cli, ["--reset-cache"])
            self.assertEqual(result.exit_code, 0)
        self.assertFalse(cache.exists())

    def test_json_full_exit_code(self) -> None:
        # The exit code must be a plain 0/1, not a count that wraps at 256.
        coords = [(
            packages.Package("p{}".format(i), "1"),
            {
                "coordinates": "pkg:pypi/p{}@1".format(i),
                "time": 1.0,
                "vulnerabilities": [{"id": str(i)}],
            },
        ) for i in range(256)]

        with patch("ossaudit.packages.get_installed",
                   return_value=[c[0] for c in coords]):
            with patch("ossaudit.audit.components", return_value=coords):
                runner = CliRunner()
                result = runner.invoke(cli.cli, ["--installed", "--json-full"])
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(len(json.loads(result.output)), 256)

    def test_json_full_clean_exit_code(self) -> None:
        coords = [(
            packages.Package("a", "1"),
            {"coordinates": "pkg:pypi/a@1", "time": 1.0, "vulnerabilities": []},
        )]

        with patch("ossaudit.packages.get_installed",
                   return_value=[c[0] for c in coords]):
            with patch("ossaudit.audit.components", return_value=coords):
                runner = CliRunner()
                result = runner.invoke(cli.cli, ["--installed", "--json-full"])
                self.assertEqual(result.exit_code, 0)
