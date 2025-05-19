# -*- coding: utf-8 -*-
# Created: 3/8/2018
# Project : OneClock
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QProgressBar
from PyQt6 import QtCore


class ClockProgress(QProgressBar):
    tomato = pyqtSignal()

    def __init__(self, parent, area):
        super(ClockProgress, self).__init__(parent)
        self.setObjectName("clock_progress")
        self._total_secs = 0
        self._passed_secs = 0
        self._left_secs = self._total_secs

        if area in (QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, QtCore.Qt.DockWidgetArea.RightDockWidgetArea):
            self.setOrientation(QtCore.Qt.Orientation.Vertical)
            self.setFixedWidth(10)
            self.setTextVisible(False)
        else:
            self.setOrientation(QtCore.Qt.Orientation.Horizontal)
            self.setFixedHeight(10)
            self.setTextVisible(False)

    def reset(self):
        self._total_secs = 0
        self._passed_secs = 0
        self._left_secs = self._total_secs
        super(ClockProgress, self).reset()

    def set_seconds(self, secs):

        self._total_secs = secs
        self._left_secs = self._total_secs
        self.setRange(0, self._total_secs)

    def on_timer(self):
        self._passed_secs += 1
        self._left_secs -= 1
        self.setValue(self._passed_secs)
        if self._passed_secs >= self._total_secs:
            self.tomato.emit()
        else:
            self.update_min_text()

    def update_min_text(self):
        mins = self._total_secs / 60
        text = "00:{}".format(str(mins).zfill(2))
        self.setFormat(text)
        self.setToolTip(text)
        self.setWhatsThis(text)
