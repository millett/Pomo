import math
from PyQt5.QtWidgets import *

from PyQt5.QtCore import QTimer, QSize, Qt
#from PyQt5.QtGui import (QProgressBar, QLabel, QFont, QVBoxLayout, QPainter, QPen, QColor, QDialog, QPushButton, QIcon,, QPixmap)
from PyQt5.QtGui import QPainter, QColor, QFont, QPen

from aqt import mw
from aqt.utils import askUser
from ..lib.config import ProfileConfig, UserConfig
from ..lib.constant import MIN_SECS
from ..lib.lang import _


class RoundProgress(QProgressBar):
    def __init__(self, parent):
        super(RoundProgress, self).__init__(parent)
        self.values = self.value()
        self.values = (self.values * 360) / 100
        self.n = self.value()
        self.label = QLabel(self)
        # self.label.setFont(QFont("courrier", math.sqrt(self.width())))
        self.v = QVBoxLayout(self)
        self.setLayout(self.v)
        self.v.addWidget(self.label)

    def setValue(self, n):
        self.n = n
        self.values = ((n * 5650) / self.maximum()) * (-1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor("darkblue"))
        painter.setPen(pen)
        pen = QPen()
        pen.setWidth(9)
        pen.setColor(QColor(240, 84, 94))
        painter.setPen(pen)
        painter.drawArc(5.1, 5.1, self.width() - 10, self.height() - 10, 1450, -5650)
        # painter.drawEllipse(0,0,100,100)
        painter.setBrush(QColor("lightblue"))
        pen = QPen()
        pen.setWidth(10)
        pen.setColor(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawArc(5.1, 5.1, self.width() - 10, self.height() - 10, 1450, self.values)
        self.update()


class RestDialog(QDialog):

    def __init__(self, parent):
        super(RestDialog, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.secs = 0
        self.pr = RoundProgress(self)
        self.pr.setObjectName("rest_progress")
        self.pr.setFixedSize(QSize(200, 200))

        self.btn_continue = QPushButton(_("IGNORE REST"), self)
        self.btn_continue.setFixedSize(QSize(100, 30))
        self.btn_continue.setObjectName("btn_ignore_rest")
        self.btn_continue.clicked.connect(self.on_btn_ignore_rest)

        self.a = 0
        self.total_secs = 0

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.to)

        self.l = QVBoxLayout(self)
        self.l.addWidget(self.pr, 0, Qt.AlignCenter)
        self.l.addWidget(self.btn_continue, 0, Qt.AlignCenter)

    def to(self):
        self.a += 1
        self.total_secs-=1
        self.pr.setValue(self.a)

        min = self.total_secs // MIN_SECS
        secs = self.total_secs - min * MIN_SECS

        self.pr.label.setText(
            "<center>" + _("REST") + "<br>" + "{}:{}".format(str(min).zfill(2), str(secs).zfill(2)) + "</center>"
        )

        if self.total_secs<=0:
            self.timer.stop()
            self.accept()

    def start(self, secs):
        self.total_secs = secs
        self.a = 0
        self.pr.setRange(0, self.total_secs)
        self.timer.start()

    # noinspection PyMethodOverriding
    def exec_(self, tomato_min):
        self.start(UserConfig.BREAK_MINUTES.get(str(tomato_min) + "MIN", 5) * MIN_SECS)
        # seams reason for 5minutes break (display?) bug
        return super(RestDialog, self).exec_()

    def reject(self):
        if self.timer.isActive():
            self.timer.stop()
        super(RestDialog, self).reject()

    def on_btn_ignore_rest(self, ):
        if askUser("""
                <p>""" + _("IGNORE REST QUESTION") + """</p>
                """, self):
            self.reject()
