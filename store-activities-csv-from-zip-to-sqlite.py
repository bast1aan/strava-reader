import sys

from bast1aan.strava_reader.adapters.sqlitestore import SqliteStore
from bast1aan.strava_reader import read_activities_csv

sqlite_store = SqliteStore('db.sqlite3')

read_activities_csv.store_activities_csv(sys.argv[1], sqlite_store)
