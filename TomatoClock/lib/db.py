import atexit
import datetime

from anki.cards import Card
from anki.db import DB
from aqt import mw
from ..lib.config import UserConfig
from ..lib.constant import MIN_SECS, DEBUG

CREATION_SQL = """
CREATE TABLE IF NOT EXISTS tomato_session
(
  id                INTEGER  NOT NULL
    PRIMARY KEY
  AUTOINCREMENT,
  deck              INT      NOT NULL,
  target_secs     INT      NOT NULL,
  tomato_dt         DATE     NOT NULL,
  started           DATETIME NOT NULL,
  ended             DATETIME ,
  answer_limit_secs INT,
  _mode INT
);

CREATE TABLE IF NOT EXISTS tomato_session_item
(
  id            INTEGER NOT NULL
    PRIMARY KEY
  AUTOINCREMENT,
  session_id    INT     NOT NULL
    CONSTRAINT session_detail_tomato_session_id_fk
    REFERENCES tomato_session (id)
      ON UPDATE CASCADE
      ON DELETE CASCADE,
  questioned  DATETIME,
  answered DATETIME,
  answer_shown DATETIME,
  answer_btn    INT,
  card_id    INT,
  note_id    INT
);
"""


class loader(object):
    def load(self, path):
        try:
            tmp = {}
            exec(open(path).read(), tmp)
            return tmp
        except:
            return None


class TomatoDB(DB):

    def __init__(self, db_path):
        super(TomatoDB, self).__init__(db_path)

        # call start functions
        list([getattr(self, _)() for _ in [func for func in dir(self) if func.startswith("_start_")]])

        # register close
        atexit.register(self.close)
        atexit.register(self.cleanup)

        self.cleanup()

    @property
    def statics(self):
        def _load_stats_mod():
            from .tomatostats import TomatoStats
            return {'TomatoStats': TomatoStats}

        if DEBUG:
            m = _load_stats_mod()
        else:
            try:
                m = loader().load("_tomatostats.py")
                if 'TomatoStats' not in list(m.keys()):
                    raise KeyError
            except:
                m = _load_stats_mod()

        return m['TomatoStats'](self, DEBUG, UserConfig)

    def _start_ensure_tables(self):
        self.executescript(CREATION_SQL)

    def cleanup(self):
        self.execute(
            """
            DELETE FROM tomato_session_item WHERE questioned IS NOT NULL
            AND (answer_shown IS  NULL
            OR answered IS  NULL);
            """
        )
        self.execute("vacuum")
        self.execute("analyze")

    @property
    def session_id(self):
        return self.scalar("SELECT seq FROM sqlite_sequence "
                           "WHERE name=?", 'tomato_session')

    @property
    def session_item_id(self):
        return self.scalar("SELECT seq FROM sqlite_sequence "
                           "WHERE name=?", 'tomato_session_item')

    @property
    def card(self):
        """

        :rtype: Card
        """
        return mw.reviewer.card

    @property
    def deck(self):
        """

        :rtype:
        """
        return mw.col.decks.current()

    @property
    def all_decks_id(self):
        return [d for d in mw.col.decks.decks]

    @property
    def now(self):
        return datetime.datetime.now()

    def execute(self, sql, *a, **ka):
        cur = super(TomatoDB, self).execute(sql, *a, **ka)
        self.commit()
        return cur

    # region Record

    def start_session(self, target_min, limit_secs, mode):
        self.execute(
            """
            INSERT INTO tomato_session(
            deck,target_secs,tomato_dt,started,ended,answer_limit_secs,_mode
            ) VALUES (?,?,?,?,NULL ,?,?)
            """, self.card.did, target_min * MIN_SECS, self.now.date(), self.now, limit_secs, mode
        )

    def question_card(self):
        if not self.session_id:
            return
        self.execute(
            """
            INSERT INTO tomato_session_item(session_id,
            questioned,
            answered,
            answer_btn,
            card_id,
            note_id)
            VALUES(?,?,NULL,NULL,?,?)
            """, self.session_id, self.now, self.card.id, self.card.nid
        )

    def answer_shown(self):
        self.execute(
            """
            UPDATE tomato_session_item SET answer_shown = ? WHERE id = ?
            """, self.now, self.session_item_id
        )

    def answer_card(self, ease):
        self.execute(
            """
            UPDATE tomato_session_item SET answered = ? ,answer_btn = ?
            WHERE id = ?
            """, self.now, ease, self.session_item_id
        )

    def end_session(self):
        if not self.session_id:
            return
        self.execute(
            """
            UPDATE tomato_session SET ended = ? WHERE id = ?
            """, self.now, self.session_id
        )

    # endregion
