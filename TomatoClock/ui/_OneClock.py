# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OneClock.ui'
#
# Created: Tue Mar 13 14:30:28 2018
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig)

class Ui_TomatoClockDlg(object):
    def setupUi(self, TomatoClockDlg):
        TomatoClockDlg.setObjectName("TomatoClockDlg")
        TomatoClockDlg.resize(313, 429)
        TomatoClockDlg.setStyleSheet("/*region OneClock*/\n"
"#TomatoClockDlg {\n"
"    font-family: \'Microsoft YaHei UI\', Consolas, serif;\n"
"}\n"
"\n"
"#frame {\n"
"    /*border: 1px solid red;*/\n"
"    border-radius: 10px;\n"
"    background-color: #3A4055;\n"
"}\n"
"\n"
"#label_remark {\n"
"    font-size: 10pt;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"#btn_clock {\n"
"    border-top-left-radius: 6px;\n"
"    border-bottom-left-radius: 6px;\n"
"    border-bottom: 1px solid white;\n"
"    border-top: 1px solid white;\n"
"    border-left: 1px solid white;\n"
"}\n"
"\n"
".QPushButton:checked {\n"
"    background-color: #f0545e;\n"
"    border: None;\n"
"}\n"
"\n"
"#btn_comp {\n"
"    border-top-right-radius: 6px;\n"
"    border-bottom-right-radius: 6px;\n"
"    border-bottom: 1px solid white;\n"
"    border-top: 1px solid white;\n"
"    border-right: 1px solid white;\n"
"}\n"
"#btn_quick {\n"
"    border-bottom: 1px solid white;\n"
"    border-top: 1px solid white;\n"
"}\n"
"\n"
"#btn_start {\n"
"    background-color: #f0545e;\n"
"    border-radius: 16px;\n"
"    font-size: 10pt;\n"
"    color: white;\n"
"}\n"
"\n"
"#btn_start:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"#btn_cancel {\n"
"    background-color: #5550f0;\n"
"    border-radius: 6px;\n"
"    font-size: 8pt;\n"
"    color: white;\n"
"}\n"
"\n"
"#btn_cancel:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"#list_mis {\n"
"    color: white;\n"
"    background: #3A4055;\n"
"    font-size: 15pt;\n"
"    alignment: center;\n"
"    border: none;\n"
"}\n"
"\n"
"/*endregion*/\n"
"\n"
"/*region Progress Bar*/\n"
"#clock_progress {\n"
"    text-align: center;\n"
"    border-radius: 3px;\n"
"    background-color: #f0545e;\n"
"    margin: 0;\n"
"}\n"
"\n"
"#clock_progress::chunk {\n"
"    background-color: #ffffff;\n"
"    width: 20px;\n"
"}\n"
"\n"
"#rest_progress {\n"
"    /*border: 2px solid grey;*/\n"
"    text-align: center;\n"
"    border-radius: 3px;\n"
"    /*width: 5px;*/\n"
"}\n"
"\n"
"#rest_progress::chunk {\n"
"    width: 20px;\n"
"}\n"
"\n"
"#rest_progress QLabel {\n"
"    border-image: url(\":/icon/tomato.png\");\n"
"    font-family: \'Microsoft YaHei UI\', serif;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 15pt;\n"
"}\n"
"\n"
"#btn_ignore_rest {\n"
"    background-color: #3A4055;\n"
"    border-radius: 10px;\n"
"    font-size: 10pt;\n"
"    color: white;\n"
"}\n"
"\n"
"#btn_ignore_rest:hover {\n"
"    border: 1px solid white;\n"
"    background-color: #f0545e;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"#btn_setting {\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#btn_setting:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"#btn_donate {\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#btn_wechat {\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#btn_donate:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"#btn_wechat:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"#btn_more_addon {\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#btn_more_addon:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"#btn_vote {\n"
"     border-radius: 8px;\n"
"}\n"
"\n"
"#btn_vote:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"#btn_updater {\n"
"    border-radius: 10px;\n"
"    background-color: #717da6;\n"
"}\n"
"\n"
"#btn_updater:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"\n"
"QPushButton::menu-indicator {\n"
"    width: 0;\n"
"}\n"
"\n"
"#more_addon_menu {\n"
"    background-color: #f0545e; /* sets background of the menu */\n"
"    border: 1px solid white;\n"
"    border-radius: 3px;\n"
"    color: white;\n"
"}\n"
"\n"
"#more_addon_menu::item {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"#more_addon_menu::item:selected {\n"
"    background-color: #f0313c;\n"
"}\n"
"\n"
"#more_addon_menu > QMenu {\n"
"    background-color: #f0545e;\n"
"    border: 1px solid white;\n"
"    border-radius: 3px;\n"
"    color: white;\n"
"}\n"
"\n"
"#more_addon_menu > QMenu::item {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"#more_addon_menu > QMenu::item:selected {\n"
"}\n"
"\n"
"/*endregion*/")
        self.gridLayout_2 = QtWidgets.QGridLayout(TomatoClockDlg)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(TomatoClockDlg)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_donate = QtWidgets.QPushButton(self.frame)
        self.btn_donate.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_donate.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_donate.setFlat(True)
        self.btn_donate.setObjectName("btn_donate")
        self.verticalLayout_3.addWidget(self.btn_donate)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_clock = QtWidgets.QPushButton(self.frame)
        self.btn_clock.setMinimumSize(QtCore.QSize(71, 71))
        self.btn_clock.setMaximumSize(QtCore.QSize(71, 71))
        self.btn_clock.setStyleSheet("")
        self.btn_clock.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/star_off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icon/star_on.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btn_clock.setIcon(icon)
        self.btn_clock.setIconSize(QtCore.QSize(48, 48))
        self.btn_clock.setCheckable(True)
        self.btn_clock.setChecked(True)
        self.btn_clock.setAutoDefault(False)
        self.btn_clock.setFlat(True)
        self.btn_clock.setObjectName("btn_clock")
        self.horizontalLayout.addWidget(self.btn_clock)
        self.btn_comp = QtWidgets.QPushButton(self.frame)
        self.btn_comp.setMinimumSize(QtCore.QSize(71, 71))
        self.btn_comp.setMaximumSize(QtCore.QSize(71, 71))
        self.btn_comp.setStyleSheet("")
        self.btn_comp.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/simple_off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icon/simple_on.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btn_comp.setIcon(icon1)
        self.btn_comp.setIconSize(QtCore.QSize(48, 48))
        self.btn_comp.setCheckable(True)
        self.btn_comp.setChecked(False)
        self.btn_comp.setAutoDefault(False)
        self.btn_comp.setFlat(True)
        self.btn_comp.setObjectName("btn_comp")
        self.horizontalLayout.addWidget(self.btn_comp)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btn_setting = QtWidgets.QPushButton(self.frame)
        self.btn_setting.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_setting.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_setting.setObjectName("btn_setting")
        self.verticalLayout_4.addWidget(self.btn_setting)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_remark = QtWidgets.QLabel(self.frame)
        self.label_remark.setMinimumSize(QtCore.QSize(0, 30))
        self.label_remark.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_remark.setText("")
        self.label_remark.setObjectName("label_remark")
        self.verticalLayout_2.addWidget(self.label_remark)
        self.list_mis = QtWidgets.QListWidget(self.frame)
        self.list_mis.setMinimumSize(QtCore.QSize(0, 0))
        self.list_mis.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_mis.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_mis.setTextElideMode(QtCore.Qt.ElideLeft)
        self.list_mis.setWordWrap(False)
        self.list_mis.setSelectionRectVisible(False)
        self.list_mis.setObjectName("list_mis")
        item = QtWidgets.QListWidgetItem()
        self.list_mis.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.list_mis.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.list_mis.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.list_mis.addItem(item)
        self.verticalLayout_2.addWidget(self.list_mis)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.btn_start = QtWidgets.QPushButton(self.frame)
        self.btn_start.setMinimumSize(QtCore.QSize(251, 41))
        self.btn_start.setMaximumSize(QtCore.QSize(251, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI,serif")
        font.setPointSize(10)
        self.btn_start.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/tomato.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_start.setIcon(icon2)
        self.btn_start.setIconSize(QtCore.QSize(36, 36))
        self.btn_start.setObjectName("btn_start")
        self.horizontalLayout_3.addWidget(self.btn_start)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.btn_cancel = QtWidgets.QPushButton(self.frame)
        self.btn_cancel.setMinimumSize(QtCore.QSize(60, 20))
        self.btn_cancel.setMaximumSize(QtCore.QSize(251, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_4.addWidget(self.btn_cancel)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(TomatoClockDlg)
        self.list_mis.setCurrentRow(-1)
        self.btn_start.clicked.connect(TomatoClockDlg.accept)
        self.btn_cancel.clicked.connect(TomatoClockDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(TomatoClockDlg)

    def retranslateUi(self, TomatoClockDlg):
        TomatoClockDlg.setWindowTitle(_translate("TomatoClockDlg", "Dialog", None))
        self.btn_donate.setText(_translate("TomatoClockDlg", "DONATE", None))
        self.btn_setting.setText(_translate("TomatoClockDlg", "PushButton", None))
        __sortingEnabled = self.list_mis.isSortingEnabled()
        self.list_mis.setSortingEnabled(False)
        item = self.list_mis.item(0)
        item.setText(_translate("TomatoClockDlg", "10 Minutes", None))
        item = self.list_mis.item(1)
        item.setText(_translate("TomatoClockDlg", "15 Minutes", None))
        item = self.list_mis.item(2)
        item.setText(_translate("TomatoClockDlg", "20 Minutes", None))
        item = self.list_mis.item(3)
        item.setText(_translate("TomatoClockDlg", "25 Minutes", None))
        self.list_mis.setSortingEnabled(__sortingEnabled)
        self.btn_start.setText(_translate("TomatoClockDlg", "Start", None))
        self.btn_cancel.setText(_translate("TomatoClockDlg", "Cancel", None))

from . import resource_rc
