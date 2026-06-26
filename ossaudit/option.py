# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

import configparser
import re
from typing import Any, Callable, Optional, Tuple

import click
from click.core import ParameterSource

from . import __project__, const


class Option(click.Option):
    sep = re.compile(r"[\n\r,]")

    def consume_value(
            self, ctx: click.Context, opts: Any
    ) -> Tuple[Any, ParameterSource]:
        """
        Consume a value, falling back to the config file when the value
        comes from the default (i.e. was not supplied on the CLI or via
        an environment variable).

        Resolution order:

        1. From command-line arguments.
        2. From `default_map`.
        3. From environment variables.
        4. From configuration files.
        5. From the `default` keyword argument.
        """
        value, source = super().consume_value(ctx, opts)
        if source in (ParameterSource.DEFAULT, ParameterSource.DEFAULT_MAP):
            name = self.name.replace("_", "-")
            config = ctx.obj and ctx.obj.get("config")
            cfg_value = config and config.get(__project__, name, fallback=None)
            if cfg_value is not None:
                if self.multiple:
                    value = tuple(
                        v.strip() for v in self.sep.split(cfg_value) if v
                    )
                else:
                    value = cfg_value
        return value, source


def add(*param_decls: str, **attrs: Any) -> Callable:
    """
    Add an option with the extended `Option` class.
    """
    return click.option(*param_decls, **attrs, cls=Option)  # type: ignore


def add_config(*param_decls: str, **attrs: Any) -> Callable:
    """
    Add an unexposed option that initializes the configuration.
    """

    def cb(ctx: click.Context, _param: Option, value: Optional[str]) -> None:
        value = value or str(const.CONFIG)
        ctx.obj = ctx.obj or {}
        ctx.obj["config"] = configparser.ConfigParser()
        try:
            ctx.obj["config"].read(value)
        except configparser.Error as e:
            raise click.ClickException(str(e))

    attrs["callback"] = cb
    attrs["expose_value"] = False
    attrs["is_eager"] = True

    return add(*param_decls, **attrs)
