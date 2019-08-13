# -*- coding:utf-8 -*-
#
# Copyright © 2016–2017 Liang Feng <finalion@gmail.com>
#
# Support: Report an issue at https://github.com/finalion/WordQuery/issues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version; http://www.gnu.org/copyleft/gpl.html.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from anki.lang import currentLang

_style = """
<style>

* {
    font-family: 'Microsoft YaHei UI', Consolas, serif;
}

</style>

"""

trans = {
    'TOMATO COLOCK': {'zh_CN': '番茄时钟', 'en': 'Tomato Clock'},
    'IGNORE REST': {'zh_CN': '跳过休息', 'en': 'Continue'},
    'REST': {'zh_CN': "休息", 'en': 'Break'},
    'IGNORE REST QUESTION': {'zh_CN': "跳过休息吗？", 'en': 'Ignore break and continue?'},
    'ABORT TOMATO': {'zh_CN': "中断番茄专注吗？", 'en': 'Abort Tomato Clock?'},
    'CANCEL': {'zh_CN': "取消", 'en': 'Back'},
    'RETURN': {'zh_CN': "返回", 'en': 'Return'},
    'MINUTES': {'zh_CN': "分钟", 'en': '5 Minutes'},
    'MIN': {'zh_CN': "分钟", 'en': '5 Minutes'},
    'MINS': {'zh_CN': "分钟", 'en': '5 Minutes'},
    'ENTER ONLY DIGITS': {'zh_CN': "请只输入数字！", 'en': 'Only digits are acceptable!'},
    'SUPPORT DEVELOPMENT': {'zh_CN': "掏出手机请框框喝咖啡吧！", 'en': 'Donate for Development'},
    'FOCUS MODE REMARK': {'zh_CN': _style + "<center>专注模式</center>",
                          'en': _style + '<center>Tomato Mode</center>'},
    'NORMAL MODE REMARK': {'zh_CN': _style + "<center>普通模式</center>",
                           'en': _style + '<center>Normal Mode</center>'},
    'QUICK MODE REMARK': {'zh_CN': _style + "<center>训练模式</center>",
                          'en': _style + '<center>Training Mode</center>'},
}


def _(key, lang=currentLang):
    key = key.upper().strip()
    if lang != 'zh_CN' and lang != 'en' and lang != 'fr':
        lang = 'en'  # fallback

    def disp(s):
        return s.lower().capitalize()

    if key not in trans or lang not in trans[key]:
        return disp(key)
    return trans[key][lang]


def _sl(key):
    return list(trans[key].values())
