import os
import pickle
import sqlite3
import tempfile
import unittest
from typing import cast

from stravalib.strava_model import DetailedActivity

from bast1aan.strava_reader.adapters.sqlitestore import SqliteStore
from bast1aan.strava_reader.adapters.stravalib import _pydantic_to_entity


class SqliteStoreTestCase(unittest.TestCase):
    def test_save_api_activity(self) -> None:
        with open('activity.pickle', 'rb') as f:
            activity = cast(DetailedActivity, pickle.loads(f.read()))
        api_activity = _pydantic_to_entity(activity)

        with tempfile.TemporaryDirectory() as tmpdirname:
            store = SqliteStore(os.path.join(tmpdirname, 'db.sqlite3'))
            with store as uow:
                uow.save_api_activity(api_activity)

            conn = sqlite3.connect(os.path.join(tmpdirname, 'db.sqlite3'), isolation_level=None)
            cur = conn.execute('SELECT * FROM api_activities');
            res = cur.fetchall()
            with open('activity_expected.pickle', 'rb') as f:
                expected = pickle.loads(f.read())
            self.assertEqual(res, expected)

