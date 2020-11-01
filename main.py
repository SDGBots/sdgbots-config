#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SCP-079-CONFIG - Manage the settings of each bot
# Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>
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
from random import randint

from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import Client

from plugins import glovar
from plugins.functions.timers import backup_files, interval_min_01, reset_data, update_status

# Enable logging
logger = logging.getLogger(__name__)

# Config session
app = Client(
    session_name="bot",
    bot_token=glovar.bot_token
)
app.start()

# Send online status
update_status(app, "online")

# Timer
scheduler = BackgroundScheduler(job_defaults={"misfire_grace_time": 60})
scheduler.add_job(interval_min_01, "interval", [app], minutes=1)
scheduler.add_job(update_status, "cron", [app, "awake"], minute=randint(30, 34), second=randint(0, 59))
scheduler.add_job(backup_files, "cron", [app], hour=20)
scheduler.add_job(reset_data, "cron", [app], day=glovar.date_reset, hour=22)
scheduler.start()

# Hold
app.idle()

# Stop
app.stop()
