import dataclasses
import sqlite3
from datetime import datetime, timedelta
import time
from typing import Sequence

from bast1aan.strava_reader.entities import Activity, Store

SQLITE_TYPE_MAP = {
	int: 'INTEGER',
	float: 'REAL',
	str: 'TEXT',
	bool: 'INTEGER',
	datetime: 'INTEGER',
	timedelta: 'INTEGER',
}

CONV_TO_SQLITE = {
	bool: lambda v: int(v),
	datetime: lambda v: time.mktime(v.timetuple()),
	timedelta: lambda v: v.seconds,
}

class SqliteStore(Store):
	TBL_FROM_BULKEXPORT_ACTIVITIES_ORIG = 'frombulkexport_activities_orig'
	TBL_FROM_BULKEXPORT_ACTIVITIES = 'frombulkexport_activities'

	_connection: sqlite3.Connection

	def __init__(self, dbpath: str):
		self._connection = sqlite3.connect(dbpath)
		self._create_table_activities_orig()
		self._create_table_activities()

	def _create_table_activities_orig(self):
		stmt = f'CREATE TABLE IF NOT EXISTS {self.TBL_FROM_BULKEXPORT_ACTIVITIES_ORIG} '
		columns = []
		for field in dataclasses.fields(Activity):
			if field.name == 'id':
				columns.append(f'id INTEGER PRIMARY KEY')
				continue
			columns.append(f'{field.name} TEXT')
		self._connection.execute(stmt + '(' + ','.join(columns) + ')')

	def _create_table_activities(self):
		stmt = f'CREATE TABLE IF NOT EXISTS {self.TBL_FROM_BULKEXPORT_ACTIVITIES} '
		columns = []
		for field in dataclasses.fields(Activity):
			if field.name == 'id':
				columns.append(f'id INTEGER PRIMARY KEY')
				continue
			columns.append(f'{field.name} {SQLITE_TYPE_MAP[field.type]}')
		self._connection.execute(stmt + '(' + ','.join(columns) + ')')

	def save_activity_as_string(self, activity: Sequence[str]) -> None:
		stmt = "INSERT INTO {tbl} VALUES({value_placeholders})".format(
			tbl=self.TBL_FROM_BULKEXPORT_ACTIVITIES_ORIG,
			value_placeholders=','.join(['?'] * len(activity))
		)
		self._connection.execute(stmt, tuple(activity))
		self._connection.commit()

	def save_activity(self, activity: Activity) -> None:
		activity_dict = dataclasses.asdict(activity)

		stmt = "INSERT INTO {tbl} ({fields}) VALUES({value_placeholders})".format(
			tbl=self.TBL_FROM_BULKEXPORT_ACTIVITIES,
			fields=','.join(activity_dict.keys()),
			value_placeholders=','.join(['?'] * len(activity_dict)),
		)

		field_types = {field.name: field.type for field in dataclasses.fields(activity)}
		items = []
		for k, v in activity_dict.items():
			field_type = field_types[k]
			if v and field_type in CONV_TO_SQLITE:
				items.append(CONV_TO_SQLITE[field_type](v))
			else:
				items.append(v)
		self._connection.execute(stmt, tuple(items))
		self._connection.commit()
