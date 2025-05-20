# -*- coding: utf-8 -*-
# Created: 3/13/2018
# Project : TomatoClock
import datetime
import json
import os
from copy import deepcopy
from operator import itemgetter
from urllib.request import urlretrieve

from PyQt6.QtCore import QUrl, QDir

trans = {
    'report days part1': {'zh_CN': '最近番茄时钟数据：', 'en': 'Recent Pomodore statistics：'},
    'days': {'zh_CN': '天', 'en': 'day(s)'},
    "'Minutes Studied'": {'zh_CN': "'学习分钟数'", 'en': "'Minutes Studied'"},
    "'Best Focus Hour'": {'zh_CN': "'最佳学习时段'", 'en': "'Best Focus Hour'"},
    "'Count of Tomatoes and Minutes'": {'zh_CN': "'番茄和学习分钟'",
                                        'en': "'Count of Tomatoes and Minutes'"},
    "'Tomato Count'": {'zh_CN': "'番茄个数'", 'en': "'Tomato Count'"},
    "'Cards'": {'zh_CN': "'卡片'", 'en': "'Cards'"},
    "'{a} <br/>{b} Clock: {c} Minutes'": {'zh_CN': "'{a} <br/>{b} 点: {c} 分钟'",
                                          'en': "'{a} <br/>{b} Clock: {c} Minutes'"},

    "total_studied_hour": {'zh_CN': '总时间（小时）', 'en': 'Total Time (Hour)'},
    "total_tomato": {'zh_CN': '总番茄钟', 'en': 'Total Tomato'},
    "today_total_min": {'zh_CN': '今日时间（分钟）', 'en': 'Today Time (Minute)'},
    "today_total_tomato": {'zh_CN': '今日番茄钟', 'en': 'Today Tomato'},
    "today_min_pctg": {'zh_CN': '今日时间完成率', 'en': 'Today Time %'},
    "today_tomato_pctg": {'zh_CN': '今日番茄完成率', 'en': 'Today Tomato %'}

}


def _(key):
    from anki.lang import currentLang
    lang = currentLang
    key = key.upper().strip()
    if lang != 'zh_CN' and lang != 'en' and lang != 'fr':
        lang = 'en'  # fallback

    def disp(s):
        return s.lower().capitalize()

    for k, v in list(trans.items()):
        trans[k.upper()] = v

    if key not in trans or lang not in trans[key]:
        return disp(key)
    return trans[key][lang]


_echart_js = "http://echarts.baidu.com/examples/vendors/echarts/echarts.min.js"


class TomatoStats:
    def __init__(self, db, debug=False, user_config=None):
        self.debug = debug
        self.user_config = user_config
        if self.debug:
            from .db import TomatoDB
            assert isinstance(db, TomatoDB)
        self.db = db
        self._data_by_dates = []
        self._recent_days = None
        self._report_type = None

    def reports(self, recent_days, report_type="current"):
        days = [7, 14, 30, 60, 180] if not self.user_config else self.user_config.report_recent_days
        self._recent_days = recent_days if recent_days else days[0]
        self._report_type = report_type

        reports_js = [
            self._chart_tomato_cnt(),
            self._chart_tomato_hour(),
            self._chart_study_minute(),
            self._chart_cards_per_tomato_cnt()
        ]
        if any(reports_js):
            (total_studied_hour, total_tomato, today_total_min, today_total_tomato,
             today_min_pctg, today_tomato_pctg) = self._numbers()

            summary_table_html = """

            <style>
                * {
                    font-family: 'Microsoft YaHei UI', Consolas, serif;
                }

                .summary_td {
                    text-align: center;
                    font-family: 'Microsoft YaHei UI', Consolas, serif;
                }

                .summary_val {
                    font-weight: bold;
                    font-size: large;
                }

                .summary_lb {
                    font-size: smaller;
                }

                .summary td {
                    /*border: 1px solid #ed1c40;*/
                    padding: 0 20px 20px 0;
                    border-radius: .25rem;
                    border-spacing: 0;
                }
            </style>
            <br>
            <table  class=summary>
            <tr>
                <td class="summary_td">
                    <span class="summary_val">%(total_studied_hour_val)s</span>
                    <br>
                    <span class="summary_lb">%(total_studied_hour)s</span>
                </td>
                <td class="summary_td">
                    <span class="summary_val">%(today_total_min_val)s</span>
                    <br>
                    <span class="summary_lb">%(today_total_min)s</span>
                </td>
                <td class="summary_td">
                    <span class="summary_val">%(today_min_pctg_val)s</span>
                    <br>
                    <span class="summary_lb">%(today_min_pctg)s</span>
                </td>

                <td class="summary_td">
                    <span class="summary_val">%(total_tomato_val)s</span>
                    <br>
                    <span class="summary_lb">%(total_tomato)s</span>
                </td>
                <td class="summary_td">
                    <span class="summary_val">%(today_total_tomato_val)s</span>
                    <br>
                    <span class="summary_lb">%(today_total_tomato)s</span>
                </td>
                <td class="summary_td">
                    <span class="summary_val">%(today_tomato_pctg_val)s</span>
                    <br>
                    <span class="summary_lb">%(today_tomato_pctg)s</span>
                </td>
            </tr>
            </table>
            """ % dict(
                total_studied_hour=_("total_studied_hour"),
                total_tomato=_("total_tomato"),
                today_total_min=_("today_total_min"),
                today_total_tomato=_("today_total_tomato"),
                today_min_pctg=_("today_min_pctg"),
                today_tomato_pctg=_("today_tomato_pctg"),

                total_studied_hour_val=total_studied_hour,
                total_tomato_val=total_tomato,
                today_total_min_val=today_total_min,
                today_total_tomato_val=today_total_tomato,
                today_min_pctg_val=today_min_pctg,
                today_tomato_pctg_val=str(round(float(today_tomato_pctg[0:-1]), 2))
            )

        return summary_table_html

    def _ref_js(self, js_source):
        js_file = "_" + os.path.basename(js_source)
        try:
            if not os.path.exists(js_file):
                urlretrieve(js_source, js_file)
            _script_src = QUrl.fromLocalFile(QDir.current().filePath(js_file)).toString()
        except Exception as exc:
            print(('Download %s failed, using CDN: %s' % (js_source, exc)))
            _script_src = js_source
        return """<script src='""" + _script_src + """'></script>"""

    @property
    def _js_ref(self):
        return self._ref_js(_echart_js)

    @property
    def _them_js_ref(self):
        return ''  # self._ref_js("http://echarts.baidu.com/asset/theme/vintage.js")#

    def _graph(self, id, conf):
        id = str(id)
        html = """
        echarts.init(document.getElementById('%(id)s'),'%(theme)s').setOption(%(conf)s);
        """ % dict(id=id, conf=json.dumps(conf).replace("\"", ""), theme='')
        return html

    @property
    def report_days(self):
        return (datetime.datetime.now() + datetime.timedelta(days=-6)).date()

    def data_by_dates(self):
        if not self._data_by_dates:
            _list_data = self.db.execute(
                """
                SELECT
                  TOMATO_DT,
                  sum(TOMATO_SECS) TT_TOMATO_SECS,
                  sum(TARGET_SECS) TT_TGT_SECS,
                  sum(TOMATO_CNT)  TT_TOMATO_CNT,
                  sum(CARDS_CNT)   TT_CARDS_COUNT,
                  sum(COMPLETE_TOMATO_CNT) TT_CMP_TOMATO_CNT,
                  count(COMPLETE_TOMATO_CNT) TT_TRIED_TOMATO_CNT
                FROM (SELECT
                        strftime('%m/%d', ts.tomato_dt)                                                    TOMATO_DT,
                        (strftime('%s', ts.ended) - strftime('%s', ts.started))                  TOMATO_SECS,
                        ts.target_secs                                                         TARGET_SECS,
                        (strftime('%s', ts.ended) - strftime('%s', ts.started)) / (ts.target_secs*1.0) TOMATO_CNT,
                        (SELECT count(*)
                         FROM tomato_session_item tsi
                         WHERE ts.id = tsi.session_id
                         and tsi.answer_btn is not null) CARDS_CNT,
                         (strftime('%s', ts.ended) - strftime('%s', ts.started)) >= ts.target_secs COMPLETE_TOMATO_CNT
                      FROM tomato_session ts
                      WHERE ended IS NOT NULL
                              AND date(ts.tomato_dt) >= ?
                              AND ts.deck in ({})
                              order by ts.tomato_dt desc)
                GROUP BY TOMATO_DT
                """.format("'" + "','".join(
                    [str(self.db.deck['id']), ] if self._report_type == 'current' else self.db.all_decks_id,
                ) + "'"), self.report_days).fetchall()

            if not _list_data:
                self._data_by_dates = [[], [], [], [], []]

            _recent_days_all = ["'%s'" % (datetime.date.today()
                                          + datetime.timedelta(0 - d)).strftime("%m/%d") for d in
                                range(self._recent_days - 1, -1, -1)]
            default_values = [0] * _recent_days_all.__len__()

            x_dt_labels = ["'%s'" % i[0] for i in _list_data]

            values_index = [i for i, days_txt in enumerate(_recent_days_all) if days_txt in x_dt_labels]

            def _refill_value(value_list):
                _ = deepcopy(default_values)
                for i, zv in enumerate(default_values):
                    if i in values_index:
                        if value_list:
                            _[i] = default_values[i] + value_list.pop(0)
                        else:
                            break
                return _

            y_tomato_min = _refill_value([round(i[1] / 60.0, 2) for i in _list_data])

            y_tomato_target_min = _refill_value([round(i[2] / 60.0, 2) for i in _list_data])
            y_tomato_count = _refill_value([round(i[3], 2) if i[3] is not None else 0 for i in _list_data])
            y_cards_count = _refill_value([round(i[4], 2) for i in _list_data])
            cmp_tomato_cnt = _refill_value([round(i[5], 2) for i in _list_data])
            tried_tomato_cnt = _refill_value([round(i[6], 2) for i in _list_data])

            self._data_by_dates = [_recent_days_all, y_tomato_count,
                                   y_tomato_min, y_tomato_target_min,
                                   y_cards_count, cmp_tomato_cnt, tried_tomato_cnt]
        return self._data_by_dates

    def _chart_study_minute(self, ):
        (x_dt_labels, y_tomato_count,
         y_tomato_min, y_tomato_target_min, y_cards_count, cmp_tomato_cnt, tried_tomato_cnt
         ) = self.data_by_dates()
        if not x_dt_labels:
            return ''

        conf = dict(
            tooltip=dict(
                trigger="'item'",
            ),
            title={
                "subtext": _("'Minutes Studied'")
            },
            xAxis=dict(data=x_dt_labels),
            yAxis={},
            series=[
                dict(
                    name=_("'Minutes Studied'"),
                    type="'bar'",
                    data=[round(m, 2) for m in y_tomato_min]
                )
            ]
        )

        return self._graph("study_minute", conf)

    def _chart_tomato_cnt(self, ):
        (x_dt_labels, y_tomato_count,
         y_tomato_min, y_tomato_target_min, y_cards_count, cmp_tomato_cnt, tried_tomato_cnt
         ) = self.data_by_dates()
        if not x_dt_labels:
            return ''

        conf = dict(
            tooltip=dict(
                trigger="'item'",
            ),
            title={
                "subtext": _("'Tomato Count'")
            },
            xAxis=dict(data=x_dt_labels),
            yAxis={},
            series=[
                dict(
                    name=_("'Tomato Count'"),
                    type="'bar'",
                    data=[round(c, 2) for c in y_tomato_count]
                )
            ]
        )

        return self._graph("tomato_cnt", conf)

    def _chart_cards_per_tomato_cnt(self):
        (x_dt_labels, y_tomato_count,
         y_tomato_min, y_tomato_target_min, y_cards_count, cmp_tomato_cnt, tried_tomato_cnt
         ) = self.data_by_dates()

        if not x_dt_labels:
            return ''

        conf = dict(
            tooltip=dict(
                trigger="'axis'",
                axisPointer=dict(
                    type="'cross'",
                    label=dict(
                        backgroundColor="'#6a7985'"
                    )
                )
            ),
            title={
                "subtext": _("'Cards'")
            },
            xAxis=dict(type="'category'",
                       data=x_dt_labels),
            yAxis=dict(type="'value'"),
            series=[dict(
                name=_("'Cards'"),
                data=[round(c, 2) for c in y_cards_count],
                type="'line'",
                smoth=True,
                label=dict(
                    normal=dict(
                        show=True,
                        position="'top'"

                    ),
                )), ]
        )

        return self._graph("cards_per_tomato_cnt", conf)

    def _chart_tomato_hour(self):
        _list_data = self.db.execute(
            """
            SELECT
              strftime('%H',ts.started)                 HOUR,
             round( sum((strftime('%s', ts.ended) - strftime('%s', ts.started)) / 60.0 ),2) MINS
            FROM tomato_session ts
            WHERE ended IS NOT NULL
                  AND ts.tomato_dt >= ?
                  AND ts.deck in ({})
            GROUP BY strftime('%H',ts.started)
            ORDER BY strftime('%H',ts.started)
            """.format("'" + "','".join(
                [str(self.db.deck['id']), ] if self._report_type == 'current' else self.db.all_decks_id,
            ) + "'"), self.report_days).fetchall()



        _list_data = sorted(_list_data, key=itemgetter(0))
        time_slots = [
            '00:00 - 07:59',
            '08:00 - 10:59',
            '11:00 - 13:59',
            '14:00 - 16:59',
            '17:00 - 21:59',
            '21:00 - 23:59',
        ]
        time_slots_range = [
            (0, 7),
            (8, 11),
            (11, 14),
            (14, 17),
            (17, 21),
            (21, 24),
        ]

        mins_stutied = [0] * time_slots.__len__()
        if _list_data:
            for i, val in enumerate(_list_data):
                min = val[1]
                for slot_i, time_slot_rng in enumerate(time_slots_range):
                    if time_slot_rng[0] <= int(val[0]) < time_slot_rng[1]:
                        mins_stutied[slot_i] = mins_stutied[slot_i] + round(min, 2)

        conf = dict(
            tooltip=dict(
                formatter=_("'{a} <br/>{b} Clock: {c} Minutes'"),
                trigger="'axis'",
                axisPointer=dict(
                    type="'cross'",
                    label=dict(
                        backgroundColor="'#6a7985'"
                    )
                )
            ),
            title={
                # "text": "'Count of Tomatoes and Minutes'",
                "subtext": _("'Best Focus Hour'")
            },
            xAxis=dict(type="'category'",
                       data=["'%s'" % i for i in time_slots]),
            yAxis=dict(type="'value'"),
            series=[dict(
                name=_("'Best Focus Hour'"),
                data=[round(m, 2) for m in mins_stutied],
                type="'line'",
                label=dict(
                    normal=dict(
                        show=True,
                        position="'top'")
                ),
                areaStyle={}), ]
        )
        return self._graph("tomato_hour", conf)

    def _numbers(self):
        (x_dt_labels, y_tomato_count,
         y_tomato_min, y_tomato_target_min, y_cards_count, cmp_tomato_cnt, tried_tomato_cnt
         ) = self.data_by_dates()

        total_studied_hour = round(sum(y_tomato_min) / 60.0, 2)
        total_tomato = round(sum(y_tomato_count), 2)

        if y_tomato_min:
            today_total_min = round(y_tomato_min[-1], 2)
        else:
            today_total_min = 0

        if y_tomato_count:
            today_total_tomato = round(y_tomato_count[-1], 2)
        else:
            today_total_tomato = 0

        # if cmp_tomato_cnt:
        #     today_total_cmp_tomato = int(cmp_tomato_cnt[-1])
        # else:
        #     today_total_cmp_tomato = 0

        if y_tomato_target_min:
            _today_targets = round(y_tomato_target_min[-1], 2)
        else:
            _today_targets = 0

        if _today_targets:
            val = round(today_total_min / _today_targets, 4) * 100
            if val >= 100:  # floating problem, not an issue
                val = 100
            today_min_pctg = "{}%".format(val)
        else:
            today_min_pctg = "0.00%"

        if tried_tomato_cnt and tried_tomato_cnt[-1]:
            today_tomato_pctg = "{}%".format(round(today_total_tomato / tried_tomato_cnt[-1], 4) * 100)
        else:
            today_tomato_pctg = "0.00%"
        return (total_studied_hour, total_tomato, today_total_min, today_total_tomato,
                today_min_pctg, today_tomato_pctg)
