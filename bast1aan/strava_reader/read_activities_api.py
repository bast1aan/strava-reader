import locale
import sys
from time import sleep

from bast1aan.strava_reader.adapters.stravalib import get_activities
from bast1aan.strava_reader.adapters.sqlitestore import SqliteStore

LOCALE = 'nl_NL.UTF8'


def main():
    after = int(sys.argv[1])
    store = SqliteStore('db.sqlite3')
    x = 0
    for activity in get_activities(after):
        with store as uow:
            uow.save_api_activity(activity)
        sleep(10.0)
        x += 1
        if x > 100:
            print(".")
            sleep(600.0)
            x = 0



if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, LOCALE)
    main()
