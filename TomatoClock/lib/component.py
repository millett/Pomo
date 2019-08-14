# -*- coding: utf-8 -*-
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

import anki.lang
from .constant import UPDATE_LOGS, __version__
from anki.lang import _
from anki.sound import play
from aqt import mw
from aqt.deckbrowser import DeckBrowser
from aqt.overview import Overview
from aqt.reviewer import Reviewer
from aqt.utils import askUser
from .config import UserConfig, ProfileConfig
from .lang import _ as _2
from ..lib.db import TomatoDB
from ..lib.lang import _ as trans, currentLang
from ..lib.sounds import ABORT, HALF_TIME, TIMEOUT
from ..ui.OneClock import OneClock


class anki_deckbrowser(DeckBrowser):

    def __init__(self, db):
        super(anki_deckbrowser, self).__init__(mw)
        self.db = db
        self.report_recent_days = None

    def reports(self):
        return self.db.statics.reports(self.report_recent_days, "all") \
            if UserConfig.SHOW_OVERALL_STATISTICS else ""

    def _linkHandler(self, url):
        if url.startswith("report_refresh"):
            self.report_recent_days = int(url.replace("report_refresh", ""))
            mw.deckBrowser.refresh()
        super(anki_deckbrowser, self)._linkHandler(url)

    _body = """
        <center>
        <table cellspacing=0 cellpading=3>
        %(tree)s
        </table>

        <br>
        %(stats)s
        %(countwarn)s

        %(tomato_summary)s
        </center>
        <script>
            $( init );

            function init() {

                $("tr.deck").draggable({
                    scroll: false,

                    // can't use "helper: 'clone'" because of a bug in jQuery 1.5
                    helper: function (event) {
                        return $(this).clone(false);
                    },
                    delay: 200,
                    opacity: 0.7
                });
                $("tr.deck").droppable({
                    drop: handleDropEvent,
                    hoverClass: 'drag-hover',
                });
                $("tr.top-level-drag-row").droppable({
                    drop: handleDropEvent,
                    hoverClass: 'drag-hover',
                });
            }

            function handleDropEvent(event, ui) {
                var draggedDeckId = ui.draggable.attr('id');
                var ontoDeckId = $(this).attr('id');

                py.link("drag:" + draggedDeckId + "," + ontoDeckId);
            }
        </script>
        """

    def _renderPage(self, reuse=False):
        if not reuse:
            self._dueTree = self.mw.col.sched.deckDueTree()
        tree = self._renderDeckTree(self._dueTree)
        stats = self._renderStats()
        self.web.stdHtml(self._body % dict(
            tomato_summary=self.reports(),
            tree=tree, stats=stats, countwarn=self._countWarn()),
            css=["deckbrowser.css"],
                        js=["jquery.js", "jquery-ui.js", "deckbrowser.js"])
        self.web.key = "deckBrowser"
        self._drawButtons()



class anki_overview(Overview):
    def __init__(self, tomato_dlg, db):
        assert isinstance(db, TomatoDB)
        assert isinstance(tomato_dlg, OneClock)
        super(anki_overview, self).__init__(mw)
        self.dlg = tomato_dlg
        self.addon_version = __version__
        self.update_logs = UPDATE_LOGS
        self.db = db
        self.report_recent_days = None

    def reports(self):
        return self.db.statics.reports(self.report_recent_days) if UserConfig.SHOW_DECK_STATISTICS else ""

    def _linkHandler(self, url):
        # if url == 'show_tomato_chart':
        #    self.web.eval("show_tomato_chart(%s);" % (self.reports(),))

        if url == 'tomato_clock':
            self.show_update_logs()
            self.dlg.btn_start.setText(anki.lang._("Study Now"))
            self.dlg.exec_()
        elif url.startswith("report_refresh"):
            self.report_recent_days = int(url.replace("report_refresh", ""))
            mw.overview.refresh()
        else:
            super(anki_overview, self)._linkHandler(url)

    def show_update_logs(self):
        if ProfileConfig.ttc_current_version != self.addon_version:
            for logs in self.update_logs:
                cur_log_ver, cur_update_msg = logs
                if cur_log_ver != self.addon_version:
                    continue
                QMessageBox.warning(mw, Pomodore, """
                <p><b>v{} {}:</b></p>
                <p>{}</p>
                """.format(cur_log_ver, "更新" if currentLang == "zh_CN" else "Update", cur_update_msg))
                ProfileConfig.ttc_current_version = self.addon_version

    def _table(self):
        counts = list(self.mw.col.sched.counts())
        finished = not sum(counts)
        for n in range(len(counts)):
            if counts[n] >= 1000:
                counts[n] = "1000+"
        but = self.mw.button
        if finished:
            return '<div style="white-space: pre-wrap;">%s</div>' % (
                self.mw.col.sched.finishedMsg())
        else:
            return '''
                    <table width=300 cellpadding=5 valign=top>
                        <tr>
                            <td align=center valign=top>
                                <table cellspacing=5>
                                    <tr><td>%s:</td><td><b><font color=#00a>%s</font></b></td></tr>
                                    <tr><td>%s:</td><td><b><font color=#C35617>%s</font></b></td></tr>
                                    <tr><td>%s:</td><td><b><font color=#0a0>%s</font></b></td></tr>
                                </table>
                            </td>
                            <td>
                                <table>
                                <tr>
                                    <td align=center>%s</td>
                                </tr>
                                <tr>
                                <td align=center>%s</td>
                                </tr>
                                </table>
                            </td>
                        </tr>

                    </table>

                    <table id=tomato_chart  align=center valign=center>
                        <td colspan=5>%s</td>
                    </table>

                    ''' % (
                anki.lang._("New"), counts[0],
                anki.lang._("Learning"), counts[1],
                anki.lang._("To Review"), counts[2],
                but("study", _("Study Now"), id="study"),
                but("tomato_clock", "Pomodore", id="study"),
                # but("show_tomato_chart", "Tomato Charts", id="tomato_chart_btn")
                self.reports()
            )


class anki_reviewer(Reviewer):

    def __init__(self, mode, db):
        assert isinstance(db, TomatoDB)
        super(anki_reviewer, self).__init__(mw)
        self.mode = mode
        self.db = db

    def restore_layouts(self):
        mw.menuBar().show()
        mw.setWindowFlags(Qt.Window)
        mw.show()
        mw.activateWindow()
        mw.toolbar.web.show()

    def _showAnswerButton(self, ):
        if not self.mode:
            self._bottomReady = True
            if not self.typeCorrect:
                self.bottom.web.setFocus()
            middle = '''
    <span class=stattxt>%s</span><br>
    <button title="%s" id=ansbut onclick='py.link(\"ans\");'>%s</button>
    ''' % (
                self._remaining(), _("Shortcut key: %s") % _("Space"), _("Show Answer"))
            # wrap it in a table so it has the same top margin as the ease buttons
            middle = "<table cellpadding=0><tr><td class=stat2 align=center>%s</td></tr></table>" % middle

            self.bottom.web.eval("showQuestion(%s,%d);" % (
                json.dumps(middle), UserConfig.ANSWER_TIMEOUT_SECONDS))
        else:
            super(anki_reviewer, self)._showAnswerButton()

    def _showQuestion(self):
        self.db.question_card()
        super(anki_reviewer, self)._showQuestion()

    def _answerCard(self, ease):
        self.db.answer_card(ease)
        super(anki_reviewer, self)._answerCard(ease)

    def _showAnswer(self):
        self.db.answer_shown()
        super(anki_reviewer, self)._showAnswer()
        if not self.mode:
            self.bottom.web.eval("stopTimer(%s);" % 0)

    def _linkHandler(self, url):
        if url == "decks":
            if UserConfig.PLAY_SOUNDS["abort"]:
                play(ABORT)
            if askUser(
                    _2("ABORT TOMATO"), mw
            ):
                self.db.end_session()
                mw.toolbar._linkHandler("decks")
                mw.deckBrowser.refresh()
        elif url == "half_time":
            if UserConfig.PLAY_SOUNDS["half_way_limit"]:
                play(HALF_TIME)
        elif url == 'timeout':
            if UserConfig.PLAY_SOUNDS["timeout"]: play(TIMEOUT)
            if UserConfig.SHOW_ANSWER_ON_CARD_TIMEOUT:
                self._showAnswer()
        else:
            super(anki_reviewer, self)._linkHandler(url)

    def NO_bottomHTML(self): #deac
        if not self.mode:
            mw.menuBar().hide()
            mw.toolbar.web.hide()
            mw.setWindowFlags(Qt.CustomizeWindowHint | Qt.Window)
            mw.show()
            mw.activateWindow()
            return """
            <style>
            body{font-family: 'Microsoft YaHei UI', serif;}
            .timer {font-family: 'Microsoft YaHei UI', serif;
                        color: #f0545e;font-weight: bold;font-size:15pt;
                        padding-left: 5px; padding-right: 5px; white-space: nowrap; }
            </style>


            <table width=100%% cellspacing=0 cellpadding=0>
                <tr>

                <td align=left valign=center width = 20%%>
                    <table >
                    <tr>
                        <td width=50 align=center valign=center class=stat>
                            <input type=image value = "%(r)s"
                                    onclick="py.link('decks');"
                                    src="qrc:/icon/tomato.png" width=32 height=32 />
                        </td>
                        <td width=50 align=center valign=center class=stat>
                            %(timer)s
                        </td>
                    <tr>
                    </table>
                </td>

                <td align=center valign=top id=middle width = 60%%>

                </td>

                <td align=left valign=center width = 20%%>
                    <span></span>
                </td>

                </tr>
            </table>
            <script>
            var time = %(time)d;
            var maxTime = -1;
            $(function () {
            $("#ansbut").focus();
            updateTime();
            setInterval(function () { time+=1;maxTime -= 1; updateTime() }, 1000);
            });

            var updateTime = function () {
                if (maxTime<0) {
                    return;
                }
                // maxTime = Math.max(maxTime, time);
                var m = Math.floor(maxTime / 60);
                var s = maxTime %% 60;
                if (s < 10) {
                    s = "0" + s;
                }
                var e = $("#time");
                if (time==maxTime){
                    py.link('half_time')
                }
                if (!maxTime) {
                    e.html("<font color=red>" + m + ":" + s + "</font>");
                    py.link('timeout')
                } else {
                    e.text(m + ":" + s);
                }
            }

            function showQuestion(txt, maxTime_) {
              // much faster than jquery's .html()
              $("#middle")[0].innerHTML = txt;
              $("#ansbut").focus();
              time = 0;
              maxTime = maxTime_;
            }

            function showAnswer(txt) {
              $("#middle")[0].innerHTML = txt;
              $("#defease").focus();
            }

            function stopTimer(maxTime_){
                $("#time").text("");
                maxTime = maxTime_;
            }

            </script>
            """ % dict(r=_2("RETURN"),
                       timer="<span id=time class=timer></span>"
                       , rem=self._remaining(),
                       time=self.card.timeTaken() // 1000)
        return super(anki_reviewer, self)._bottomHTML()

    def _initWeb(self):
        super(anki_reviewer, self)._initWeb()

        # region ensure html  is shown ...

        self._showAnswerButton()

        # warning below is just an copy of _showQuestion function of anki2.0.48
        # to execute this because the reviewer and bottm html cannot be shown at the first time

        c = self.card
        # grab the question and play audio
        if c.isEmpty():
            q = _("""The front of this card is empty. Please run Tools>Empty Cards.""")
        else:
            q = c.q()
        # render & update bottom
        q = self._mungeQA(q)
        klass = "card card%d" % (c.ord + 1)
        self.web.eval("_updateQA(%s, false, '%s');" % (json.dumps(q), klass))

        # endregion
