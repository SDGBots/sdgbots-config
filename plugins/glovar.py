# SCP-079-CONFIG - Manage the settings of each bot
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-CONFIG.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from configparser import RawConfigParser
from typing import Dict, List, Union

# Enable logging
logger = logging.getLogger(__name__)

# Init

all_commands: List[str] = ["version"]

configs: Dict[str, Dict[str, Union[int, dict, str]]] = {}
# configs = {
#     "random": {
#         "type": "warn",
#         "group_id": -10012345678,
#         "group_name": "Group Name",
#         "group_link": "link to group",
#         "user_id": 12345678,
#         "message_id": 123,
#         "config": {
#             "default": True
#             "limit": 3,
#             "locked": 0,
#             "mention": False,
#             "report": {
#                 "auto": False,
#                 "manual": False
#             }
#         }
#     }
# }

version = "0.0.4"

# Read data from config.ini

# [basic]
bot_token: str = ""
prefix: List[str] = []
prefix_str: str = "/!"

# [channels]
config_channel_id: int = 0
debug_channel_id: int = 0
exchange_channel_id: int = 0
test_group_id: int = 0

# [custom]
noporn_link: str = ""
noporn_name: str = ""
warn_link: str = ""
warn_name: str = ""

try:
    config = RawConfigParser()
    config.read("config.ini")
    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = list(config["basic"].get("prefix", prefix_str))
    # [channels]
    config_channel_id = int(config["channels"].get("config_channel_id", config_channel_id))
    debug_channel_id = int(config["channels"].get("debug_channel_id", debug_channel_id))
    exchange_channel_id = int(config["channels"].get("exchange_channel_id", exchange_channel_id))
    test_group_id = int(config["channels"].get("test_group_id", test_group_id))
    # [custom]
    noporn_link = config["custom"].get("noporn_link", noporn_link)
    noporn_name = config["custom"].get("noporn_name", noporn_name)
    warn_link = config["custom"].get("warn_link", warn_link)
    warn_name = config["custom"].get("warn_name", warn_name)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

logger.warning(test_group_id)

# Check
if (bot_token in {"", "[DATA EXPUNGED]"}
        or prefix == []
        or config_channel_id == 0
        or debug_channel_id == 0
        or exchange_channel_id == 0
        or test_group_id == 0
        or noporn_link in {"", "[DATA EXPUNGED]"}
        or noporn_name in {"", "[DATA EXPUNGED]"}
        or warn_link in {"", "[DATA EXPUNGED]"}
        or warn_name in {"", "[DATA EXPUNGED]"}):
    raise SystemExit('No proper settings')

# Start program
copyright_text = (f"SCP-079-CONFIG v{version}, Copyright (C) 2019 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
