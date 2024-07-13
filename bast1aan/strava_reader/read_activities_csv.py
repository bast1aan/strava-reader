import csv
import locale
import sys
import zipfile
import dataclasses
from pprint import pprint

from datetime import datetime, timedelta, timezone
from io import TextIOWrapper
from typing import Iterator, TypeVar, Callable, Mapping

from bast1aan.strava_reader.entities import Activity, Store

FIELDS_MAPPING_NL = (
	('Activiteits-ID', 'id'),
	('Datum van activiteit', 'date'),
	('Naam activiteit', 'name'),
	('Activiteitstype', 'type'),
	('Beschrijving van activiteit', 'description'),
	('Verstreken tijd', 'elapsed_time'),
	('Afstand', 'distance'),
	('Max. hartslag', 'bpm_max'),
	('Vergelijkbare poging', 'comparing_try'),
	('Woon-werkverkeer', 'commute'),
	('Privénotitie activiteit', 'private_note'),
	('Uitrusting voor activiteit', 'gear'),
	('Bestandsnaam', 'file'),
	('Gewicht sporter', 'athlete_weight'),
	('Gewicht fiets', 'bicycle_wieght'),
	('Verstreken tijd', 'elapsed_time2'),
	('Beweegtijd', 'moving_time'),
	('Afstand', 'distance2'),
	('Max. snelheid', 'speed_max'),
	('Gemiddelde snelheid', 'speed_avg'),
	('Totale stijging', 'ascend_total'),
	('Totale daling', 'descend_total'),
	('Kleinste hoogte', 'lowest_altitude'),
	('Grootste hoogte', 'highest_altitude'),
	('Max. stijgingspercentage', 'slope_max'),
	('Gemiddeld stijgingspercentage', 'slope_avg'),
	('Gemiddeld positief stijgingspercentage', 'slope_avg_up'),
	('Gemiddeld negatief stijgingspercentage', 'slope_avg_down'),
	('Max. cadans', 'rpm_max'),
	('Gemiddelde cadans', 'rpm_avg'),
	('Max. hartslag', 'bpm_max2'),
	('Gemiddelde hartslag', 'bpm_avg2'),
	('Maximaal wattage', 'power_max'),
	('Gemiddeld wattage', 'power_avg'),
	('Calorieën', 'calories'),
	('Maximale temperatuur', 'temperature_max'),
	('Gemiddelde temperatuur', 'temperature_avg'),
	('Vergelijkbare poging', 'comparing_try2'),
	('Totale arbeid', 'work_total'),
	('Aantal hardloopsessies', 'runner_sessions_amount'),
	('Tijd bergop', 'time_ascending'),
	('Tijd bergaf', 'time_descending'),
	('Andere tijd', 'other_time'),
	('Ervaren inspanning', 'experienced_intensity'),
	('Type', 'type2'),
	('Starttijd', 'start'),
	('Gewogen gemiddeld vermogen', 'power_avg_weighted'),
	('Aantal vermogensgegevens', 'power_sensor_amount'),
	('Voorkeur voor ervaren inspanning', 'preference_for_experienced_exercise'),
	('Ervaren vergelijkbare poging', 'comparing_try_for_experienced'),
	('Woon-werkverkeer', 'commute2'),
	('Totaal geheven gewicht', 'total_lifted_weight'),
	('Van upload', 'is_uploaded'),
	('Aan stijgingspercentage aangepaste afstand', 'distance_adjusted_to_slope'),
	('Tijd weerbeeld', 'weather_timestamp'),
	('Weersomstandigheden', 'weather_circumstances'),
	('Buitentemperatuur', 'outside_temperature'),
	('Gevoelstemperatuur', 'perceived_temperature'),
	('Dauwpunt', 'dew_point'),
	('Vochtigheid', 'humidity'),
	('Luchtdruk', 'atmospheric_pressure'),
	('Windsnelheid', 'wind_speed'),
	('Windstoot', 'wind_speed_max'),
	('Windrichting', 'wind_direction'),
	('Neerslagintensiteit', 'precipitation'),
	('Tijd zonsopgang', 'dusk'),
	('Tijd zonsondergang', 'dawn'),
	('Maanstand', 'moon'),
	('Fiets', 'bicycle'),
	('Uitrusting', 'gear2'),
	('Kans op neerslag', 'precipitation_probabilty'),
	('Type neerslag', 'precipitation_type'),
	('Bewolking', 'cloud_cover'),
	('Zicht', 'vision'),
	('UV-index', 'uv_index'),
	('Ozonwaarde', 'ozone'),
	('Aantal jumps', 'jumps_count'),
	('Totale grit', 'grit_total'),
	('Gemiddelde flow', 'average_flow'),
	('Gemeld', 'flagged'),
	('Gemiddelde snelheid (op basis van verstreken tijd)', 'speed_avg_from_elapsed_time'),
	('Afstand (onverharde wegen)', 'distance_unpaved'),
	('Afstand nieuw ontdekte wegen', 'distance_new_roads'),
	('Afstand op nieuw ontdekte wegen (onverhard)', 'distance_new_roads_unpaved'),
	('Aantal activiteiten', 'activity_count'),
	('Totaal aantal stappen', 'steps'),
	('CO2-besparing', 'co2_saved'),
	('Lengte van zwembad', 'swimming_pool_length'),
	('Trainingsbelasting', 'training_impact'),
	('Intensiteit', 'intensity'),
	('Gemiddelde vergelijkbare tempo op vlak terrein', 'avg_speed_on_flat_terrain'),
	('Tijd op de timer', 'time_from_timer'),
	('Totaalaantal cycli', 'cyclus_count'),
	('Media', 'media')
)

DATE_FORMATS_NL = ('%d %b. %Y %H:%M:%S', '%d %b %Y %H:%M:%S')

DATE_FORMATS = DATE_FORMATS_NL

LOCALE = 'nl_NL.UTF8'

FIELDS_MAPPING = FIELDS_MAPPING_NL

ACTIVITY_FIELDS = dataclasses.fields(Activity)

ACTIVITY_FIELD_BY_NAME = {field.name: field for field in ACTIVITY_FIELDS}

T = TypeVar('T')

def convert_by_type(v: str, t: type[T]) -> T:
	def parseint(v_: str) -> int:
		if '.' in v_:
			v_ = v_[:v_.index('.')]
		return int(v_)

	def parsedatetime(v_: str) -> datetime:
		exceptions = []
		for date_format in DATE_FORMATS:
			try:
				return datetime.strptime(v_, date_format).replace(tzinfo=timezone.utc)
			except ValueError as e:
				exceptions.append(e)
		try:
			return datetime.utcfromtimestamp(float(v_))
		except ValueError as e:
			exceptions.append(e)
			raise ValueError(f'Cannot parse string {v_} to datetime') from exceptions

	CONVERT_BY_TYPE: Mapping[type[T], Callable[[str], T]] = {
		str: lambda v: v,
		datetime: parsedatetime,
		timedelta: lambda v: timedelta(seconds=float(v)),
		float: lambda v: float(v.replace(',', '.')),
		int: parseint,
	}
	converter = CONVERT_BY_TYPE.get(t)
	return converter(v) if converter else t(v)

def read_activities_from_zip(filepath: str) -> Iterator[list[str]]:
	with zipfile.ZipFile(filepath, 'r') as archive:
		with TextIOWrapper(archive.open('activities.csv'), newline='') as csvfile:
			reader = csv.reader(csvfile)
			next(reader)  # skip header row
			for row in reader:
				yield row

def row_to_activity(row: list[str]) -> Activity:
	activity = {}
	for i, v in enumerate(row):
		csv_field_name, activity_field_name = FIELDS_MAPPING[i]
		field = ACTIVITY_FIELD_BY_NAME[activity_field_name]
		try:
			value = convert_by_type(v, field.type) if v else None
		except ValueError as e:
			raise ValueError(f'problem converting csv field \'{csv_field_name}\' (position {i}) to Activity field `{activity_field_name}`') from e
		activity[activity_field_name] = value
	try:
		return Activity(**activity)
	except TypeError as e:
		raise TypeError(f'Error creating activity from row: {activity}') from e

def store_activities_csv(zipfile: str, store: Store) -> None:
	locale.setlocale(locale.LC_TIME, LOCALE)
	with store as uow:
		for row in read_activities_from_zip(zipfile):
			activity = row_to_activity(row)
			uow.save_activity_as_string(row)
			uow.save_activity(activity)

def print_activities(filepath: str) -> None:
	for activity in read_activities_from_zip(filepath):
		pprint(dataclasses.asdict(row_to_activity(activity)), sort_dicts=False)

if __name__ == '__main__':
	locale.setlocale(locale.LC_TIME, LOCALE)
	print_activities(sys.argv[1])
