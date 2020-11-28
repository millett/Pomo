# -*- coding: utf-8 -*-
import os
import re
from PyQt5.QtWidgets import *
from functools import partial

from PyQt5.QtCore import Qt
#from PyQt5.QtGui import QListWidgetItem, QDialog, QIcon, QPixmap
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *

from anki.sound import play
from aqt import mw
from ._OneClock import Ui_TomatoClockDlg
from ..lib.config import UserConfig
from ..lib.constant import __version__, ADDON_CD
from ..lib.lang import _
from ..lib.sounds import START
from ..lib.kkLib import AddonUpdater, UpgradeButton, ConfigEditor, VoteButton
from .Config import ConfigDialog


class OneClock(QDialog, Ui_TomatoClockDlg):

    def __init__(self, parent):
        super(OneClock, self).__init__(parent)
        self.setupUi(self)
        self._adjust_ui()
        self._mode = 0

        self.btn_clock.toggled.connect(partial(self.on_mode_toggled, 0))
        self.btn_comp.toggled.connect(partial(self.on_mode_toggled, 1))

        self.btn_clock.toggle()
        self.btn_clock.toggle()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val):
        if not val:
            self.btn_clock.setChecked(True)
            self.btn_comp.setChecked(False)
            self.label_remark.setText(_("FOCUS MODE REMARK"))
        elif val == 1:
            self.btn_clock.setChecked(False)
            self.btn_comp.setChecked(True)
            self.label_remark.setText(_("NORMAL MODE REMARK"))
        self._mode = val

    @property
    def _min_items(self):
        """

        :rtype: list of QListWidgetItem
        """
        return self.list_mis.findItems('\d.+', Qt.MatchRegExp)

    @property
    def min_item(self):
        return [i for i in self._min_items if i.isSelected()][0]

    @property
    def min(self):
        """

        :rtype: int
        """
        return int(re.match("\d+", self.min_item.text()).group())

    def _adjust_ui(self):
        self._adjust_min_list()
        self._adjust_dialog()
        self.config_dlg = ConfigDialog(self, )
        self.btn_setting.setIcon(QIcon(QPixmap(":icon/setting.png")))
        self.btn_setting.setText("")
        self.btn_setting.clicked.connect(self.on_config)

        self.updater = AddonUpdater(
            self,
            _("POMODORE"),
            ADDON_CD,
            "https://github.com/millett/pomo/blob/master/TomatoClock/lib/constant.py",
            "",
            mw.pm.addonFolder(),
            __version__
        )
        ### change ADDON_CD
        self.verticalLayout_4.insertWidget(0, VoteButton(self, ADDON_CD))
        self.verticalLayout_4.insertWidget(0, UpgradeButton(self, self.updater))

    def _adjust_dialog(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle(_("POMODORE"))

        self.btn_cancel.setText(_(self.btn_cancel.text()))
        list(
            [item.setText("{} {}".format(re.match("\d+", item.text()).group(),
                                                          _("MIN"))) for item in self._min_items]
        )

    def _adjust_min_list(self):
        break_min_dicts = UserConfig.BREAK_MINUTES
        sorted_keys = sorted(break_min_dicts.keys())

        self.list_mis.clear()
        self.list_mis.addItems(sorted_keys)

        # adjust item alignment
        list([item.setTextAlignment(Qt.AlignCenter) for item in self._min_items])
        # set default item
        self._min_items[2].setSelected(True)

    def on_mode_toggled(self, mode, toggled):
        if toggled:
            self.mode = mode

    def on_config(self, _):
        self.config_dlg.exec_()
        self._adjust_min_list()
        self._adjust_dialog()

    def exec_(self):
        if not self.updater.isRunning():
            self.updater.start()
        if UserConfig.PLAY_SOUNDS["start"]:
            play(START)
        return super(OneClock, self).exec_()
