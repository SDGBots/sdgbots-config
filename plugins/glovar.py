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
import pickle
from configparser import RawConfigParser
from os import mkdir
from os.path import exists
from shutil import rmtree
from typing import Dict, List, Union

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    filename='log',
    filemode='w'
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [basic]
bot_token: str = ""
prefix: List[str] = []
prefix_str: str = "/!"

# [channels]
config_channel_id: int = 0
critical_channel_id: int = 0
debug_channel_id: int = 0
exchange_channel_id: int = 0
hide_channel_id: int = 0
test_group_id: int = 0

# [custom]
backup: Union[str, bool] = ""
date_reset: str = ""
project_link: str = ""
project_name: str = ""
zh_cn: Union[str, bool] = ""

# [encrypt]
password: str = ""

try:
    config = RawConfigParser()
    config.read("config.ini")
    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = list(config["basic"].get("prefix", prefix_str))
    # [channels]
    config_channel_id = int(config["channels"].get("config_channel_id", config_channel_id))
    critical_channel_id = int(config["channels"].get("critical_channel_id", critical_channel_id))
    debug_channel_id = int(config["channels"].get("debug_channel_id", debug_channel_id))
    exchange_channel_id = int(config["channels"].get("exchange_channel_id", exchange_channel_id))
    hide_channel_id = int(config["channels"].get("hide_channel_id", hide_channel_id))
    test_group_id = int(config["channels"].get("test_group_id", test_group_id))
    # [custom]
    backup = config["custom"].get("backup", backup)
    backup = eval(backup)
    date_reset = config["custom"].get("date_reset", date_reset)
    project_link = config["custom"].get("project_link", project_link)
    project_name = config["custom"].get("project_name", project_name)
    zh_cn = config["custom"].get("zh_cn", zh_cn)
    zh_cn = eval(zh_cn)
    # [encrypt]
    password = config["encrypt"].get("password", password)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

# Check
if (bot_token in {"", "[DATA EXPUNGED]"}
        or prefix == []
        or config_channel_id == 0
        or critical_channel_id == 0
        or debug_channel_id == 0
        or exchange_channel_id == 0
        or hide_channel_id == 0
        or test_group_id == 0
        or backup not in {False, True}
        or date_reset in {"", "[DATA EXPUNGED]"}
        or project_link in {"", "[DATA EXPUNGED]"}
        or project_name in {"", "[DATA EXPUNGED]"}
        or zh_cn not in {False, True}
        or password in {"", "[DATA EXPUNGED]"}):
    logger.critical("No proper settings")
    raise SystemExit("No proper settings")

# Languages
lang: Dict[str, str] = {
    # Basic
    "project": (zh_cn and "项目编号") or "Project",
    "colon": (zh_cn and "：") or ": ",
    "result": (zh_cn and "结果") or "Result",
    "group_name": (zh_cn and "群组名称") or "Group Name",
    "group_id": (zh_cn and "群组 ID") or "Group ID",
    "admin_group": (zh_cn and "群管理") or "Group Admin",
    "action": (zh_cn and "执行操作") or "Action",
    "description": (zh_cn and "说明") or "Description",
    "status": (zh_cn and "状态") or "Status",
    "admin": (zh_cn and "管理员") or "Admin",
    "version": (zh_cn and "版本") or "Version",
    # Emergency
    "issue": (zh_cn and "发现状况") or "Issue",
    "exchange_invalid": (zh_cn and "数据交换频道失效") or "Exchange Channel Invalid",
    "auto_fix": (zh_cn and "自动处理") or "Auto Fix",
    "protocol_1": (zh_cn and "启动 1 号协议") or "Initiate Protocol 1",
    "transfer_channel": (zh_cn and "频道转移") or "Transfer Channel",
    "emergency_channel": (zh_cn and "应急频道") or "Emergency Channel",
    # Common
    "default_config": (zh_cn and "默认设置") or "Default Settings",
    "delete": (zh_cn and "协助删除") or "Help Delete",
    "commit": (zh_cn and "提交") or "Commit",
    # CAPTCHA
    "captcha_auto": (zh_cn and "自动免验证") or "Auto Pass",
    # CLEAN
    "con": (zh_cn and "联系人") or "Contact",
    "loc": (zh_cn and "定位") or "Location",
    "vdn": (zh_cn and "圆视频") or "Round Video",
    "voi": (zh_cn and "语音") or "Voice",
    "ast": (zh_cn and "动态贴纸") or "Animated Sticker",
    "aud": (zh_cn and "音频") or "Audio",
    "bmd": (zh_cn and "命令") or "Bot Command",
    "doc": (zh_cn and "文件") or "Document",
    "gam": (zh_cn and "游戏") or "Game",
    "gif": (zh_cn and "动图") or "GIF",
    "via": (zh_cn and "通过 Bot") or "Via Bot",
    "vid": (zh_cn and "视频") or "Video",
    "ser": (zh_cn and "服务") or "Service",
    "sti": (zh_cn and "贴纸") or "Sticker",
    "aff": (zh_cn and "推广链接") or "AFF Link",
    "exe": (zh_cn and "执行文件") or "Executable File",
    "iml": (zh_cn and "IM 链接") or "IM Link",
    "sho": (zh_cn and "短链接") or "Short Link",
    "tgl": (zh_cn and "TG 链接") or "Telegram Link",
    "tgp": (zh_cn and "TG 代理") or "Telegram Proxy",
    "qrc": (zh_cn and "二维码") or "QR Code",
    "sde": (zh_cn and "自助删除") or "Self Delete Messages",
    "tcl": (zh_cn and "定时清群") or "Clean Members Everyday",
    "ttd": (zh_cn and "定时贴纸") or "Schedule to Delete Stickers",
    # LANG
    "name_default": (zh_cn and "默认名称设置") or "Default Name Setting",
    "name_enable": (zh_cn and "检查消息名称") or "Check Message's Name",
    "text_default": (zh_cn and "默认文字设置") or "Default text Setting",
    "text_enable": (zh_cn and "检查消息文字") or "Check Message's Text",
    "sticker_default": (zh_cn and "默认贴纸设置") or "Default Sticker Setting",
    "sticker_enable": (zh_cn and "检查贴纸标题") or "Check Sticker's Title",
    # LONG
    "long_limit": (zh_cn and "消息字节上限") or "The Limit of Message's Bytes Length",
    # NOFLOOD
    "noflood_time": (zh_cn and "检测时间秒数") or "Time in seconds",
    "noflood_limit": (zh_cn and "消息条数上限") or "Message Count Limit",
    # NOPORN
    "noporn_channel": (zh_cn and "过滤频道") or "Check Restricted Channel Message",
    # NOSPAM
    "ml": (zh_cn and "机器学习") or "Machine Learning",
    "bot": (zh_cn and "阻止机器人进群") or "Prevent Bot joining",
    "deleter": (zh_cn and "仅删除") or "Delete Only",
    "reporter": (zh_cn and "仅举报") or "Report Only",
    # TIP
    "ot": (zh_cn and "群员 OT 警告") or "OT Warning by Members",
    "welcome": (zh_cn and "欢迎信息") or "Welcome Message",
    "rm": (zh_cn and "RM 警告") or "RM Jokes Warning",
    "custom": (zh_cn and "自定义关键词") or "Custom keywords",
    # USER
    "subscribe": (zh_cn and "订阅封禁") or "Subscribe Ban List",
    # WARN
    "warn_limit": (zh_cn and "警告上限") or "Warn Limit",
    "warn_admin": (zh_cn and "呼叫管理") or "Call Admins",
    "report_auto": (zh_cn and "自动举报") or "Auto Report",
    "report_manual": (zh_cn and "手动举报") or "Manual Report",
    # Special
    "committed": (zh_cn and "已更新设置") or "Committed",
    "commit_change": (zh_cn and "提交设置") or "Commit Change",
    "target": (zh_cn and "针对项目") or "Target Project",
    "config_description": ((zh_cn and "请在此进行设置，如设置完毕请点击提交，本会话将在 5 分钟后失效")
                           or ("Please change settings here. If the it is completed, please click Submit. "
                               "This session will expire after 5 minutes")),
    "config_code": (zh_cn and "设置编号") or "Config",
    "expired": (zh_cn and "会话已失效") or "Session Expired"
}

# Init

all_commands: List[str] = ["version"]

sender: str = "CONFIG"

should_hide: bool = False

version: str = "0.2.1"

# Load data from pickle

# Init dir
try:
    rmtree("tmp")
except Exception as e:
    logger.info(f"Remove tmp error: {e}")

for path in ["data", "tmp"]:
    if not exists(path):
        mkdir(path)


# Init data variables

configs: Dict[str, Dict[str, Union[bool, int, dict, str]]] = {}
# configs = {
#     "random": {
#         "type": "warn",
#         "lock": False,
#         "commit": False,
#         "time": 1512345678,
#         "group_id": -10012345678,
#         "group_name": "Group Name",
#         "group_link": "link to group",
#         "user_id": 12345678,
#         "message_id": 123,
#         "config": {
#             "default": False,
#             "lock": 1512345678,
#             "delete": True,
#             "limit": 3,
#             "mention": True,
#             "report": {
#                 "auto": True,
#                 "manual": True
#             }
#         },
#         "default": {
#             "default": True,
#             "lock": 0,
#             "delete": True,
#             "limit": 3,
#             "mention": True,
#             "report": {
#                 "auto": False,
#                 "manual": True
#             }
#         }
#     }
# }

# Load data
file_list: List[str] = ["configs"]
for file in file_list:
    try:
        try:
            if exists(f"data/{file}") or exists(f"data/.{file}"):
                with open(f"data/{file}", 'rb') as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"data/{file}", 'wb') as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)
            with open(f"data/.{file}", 'rb') as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
