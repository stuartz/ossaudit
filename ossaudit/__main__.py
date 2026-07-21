# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from . import cli, const


def main() -> None:
    prefix = const.APP_NAME.upper()
    cli.cli(auto_envvar_prefix=prefix)  # pylint: disable=E1120,E1123


if __name__ == "__main__":
    main()
