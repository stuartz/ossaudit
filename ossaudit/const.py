# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

import appdirs

# Stable app id for on-disk paths, kept separate from the distributable
# `__project__` name so config/cache locations survive package renames
# (e.g. the "ossaudit" -> "ossaudit-ng" rebrand).
APP_NAME = "ossaudit"

API = "https://api.guide.sonatype.com/api/v3/"
COMPONENT_REPORT = "component-report"
MAX_PACKAGES = 128
CONFIG = Path(appdirs.user_config_dir(APP_NAME)).joinpath("config.ini")
CACHE = Path(appdirs.user_cache_dir(APP_NAME)).joinpath("cache.json")
CACHE_TIME = 60 * 60 * 12
REQ_TIMEOUT = 30
