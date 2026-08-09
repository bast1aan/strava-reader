from abc import abstractmethod
from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Sequence, Literal


class Store(AbstractContextManager):
	@abstractmethod
	def save_activity_as_string(self, activity: Sequence[str]) -> None:...
	@abstractmethod
	def save_activity(self, activity: Activity) -> None: ...
	@abstractmethod
	def save_api_activity(self, activity: ApiActivity) -> None: ...


@dataclass
class Activity:
	id: int  #'Activiteits-ID',
	date: datetime 	#'Datum van activiteit',
	name: str	#'Naam activiteit',
	type: str #'Activiteitstype',
	description: str #'Beschrijving van activiteit',
	elapsed_time: timedelta #'Verstreken tijd',
	distance: float #'Afstand',
	bpm_max: float # 'Max. hartslag',
	comparing_try: int #'Vergelijkbare poging',
	commute: bool  # 'Woon-werkverkeer',
	private_note: str # 'Privénotitie activiteit',
	gear: str # 'Uitrusting voor activiteit',
	file: str # 'Bestandsnaam',
	athlete_weight: float # 'Gewicht sporter',
	bicycle_wieght: float # 'Gewicht fiets',
	elapsed_time2: timedelta # 'Verstreken tijd',
	moving_time: timedelta # 'Beweegtijd',
	distance2: float # 'Afstand',
	speed_max: float # 'Max. snelheid',
	speed_avg: float # 'Gemiddelde snelheid',
	ascend_total: float # 'Totale stijging',
	descend_total: float # 'Totale daling',
	lowest_altitude: float # 'Kleinste hoogte',
	highest_altitude: float # 'Grootste hoogte',
	slope_max: float # 'Max. stijgingspercentage',
	slope_avg: float # 'Gemiddeld stijgingspercentage',
	slope_avg_up: float # 'Gemiddeld positief stijgingspercentage',
	slope_avg_down: float # 'Gemiddeld negatief stijgingspercentage',
	rpm_max: float #'Max. cadans',
	rpm_avg: float # 'Gemiddelde cadans',
	bpm_max2: float # 'Max. hartslag',
	bpm_avg2: float # 'Gemiddelde hartslag',
	power_max: float # 'Maximaal wattage',
	power_avg: float # 'Gemiddeld wattage',
	calories: float # 'Calorieën',
	temperature_max: float # 'Maximale temperatuur',
	temperature_avg: float # 'Gemiddelde temperatuur',
	comparing_try2: int  # 'Vergelijkbare poging',
	work_total: float # 'Totale arbeid',
	runner_sessions_amount: int # 'Aantal hardloopsessies',
	time_ascending: timedelta  # 'Tijd bergop',
	time_descending: timedelta # 'Tijd bergaf',
	other_time: timedelta # 'Andere tijd',
	experienced_intensity: int # 'Ervaren inspanning',
	type2: str #'Type',
	start: datetime # 'Starttijd',
	power_avg_weighted: float #'Gewogen gemiddeld vermogen',
	power_sensor_amount: int #'Aantal vermogensgegevens',
	preference_for_experienced_exercise: str # 'Voorkeur voor ervaren inspanning',
	comparing_try_for_experienced: int #'Ervaren vergelijkbare poging',
	commute2: bool # 'Woon-werkverkeer',
	total_lifted_weight: str # 'Totaal geheven gewicht',
	is_uploaded: bool # 'Van upload',
	distance_adjusted_to_slope: float #'Aan stijgingspercentage aangepaste afstand',
	weather_timestamp: datetime # 'Tijd weerbeeld',
	weather_circumstances: str # 'Weersomstandigheden',
	outside_temperature: float #'Buitentemperatuur',
	perceived_temperature: float # 'Gevoelstemperatuur',
	dew_point: float # 'Dauwpunt',
	humidity: float # 'Vochtigheid',
	atmospheric_pressure: float #'Luchtdruk',
	wind_speed: float  # 'Windsnelheid',
	wind_speed_max: float # 'Windstoot',
	wind_direction: str # 'Windrichting',
	precipitation: float # 'Neerslagintensiteit',
	dusk: datetime # 'Tijd zonsopgang',
	dawn: datetime # 'Tijd zonsondergang',
	moon: str # 'Maanstand',
	bicycle: str # 'Fiets',
	gear2: str #  'Uitrusting',
	precipitation_probabilty: str #'Kans op neerslag',
	precipitation_type: str # 'Type neerslag',
	cloud_cover: str # 'Bewolking',
	vision: float # 'Zicht',
	uv_index: float # 'UV-index',
	ozone: float # 'Ozonwaarde',
	jumps_count: int # 'Aantal jumps',
	grit_total: int # 'Totale grit',
	average_flow: float #'Gemiddelde flow',
	flagged: bool # 'Gemeld',
	speed_avg_from_elapsed_time: float # 'Gemiddelde snelheid (op basis van verstreken tijd)',
	distance_unpaved: float # 'Afstand (onverharde wegen)',
	distance_new_roads: float #'Afstand nieuw ontdekte wegen',
	distance_new_roads_unpaved: float #'Afstand op nieuw ontdekte wegen (onverhard)',
	activity_count: int #'Aantal activiteiten',
	steps: int #'Totaal aantal stappen',
	co2_saved: float # 'CO2-besparing',
	swimming_pool_length: float #'Lengte van zwembad',
	training_impact: float # 'Trainingsbelasting',
	intensity: float # 'Intensiteit',
	avg_speed_on_flat_terrain: float #'Gemiddelde vergelijkbare tempo op vlak terrein',
	time_from_timer: timedelta # 'Tijd op de timer',
	cyclus_count: int #'Totaalaantal cycli',
	media: str # 'Media',


type SportType = Literal[
	"AlpineSki",
	"BackcountrySki",
	"Badminton",
	"Basketball",
	"Canoeing",
	"Cricket",
	"Crossfit",
	"Dance",
	"EBikeRide",
	"Elliptical",
	"EMountainBikeRide",
	"Golf",
	"GravelRide",
	"Handcycle",
	"HighIntensityIntervalTraining",
	"Hike",
	"IceSkate",
	"InlineSkate",
	"Kayaking",
	"Kitesurf",
	"MountainBikeRide",
	"NordicSki",
	"Padel",
	"PhysicalTherapy",
	"Pickleball",
	"Pilates",
	"Racquetball",
	"Ride",
	"RockClimbing",
	"RollerSki",
	"Rowing",
	"Run",
	"Sail",
	"Skateboard",
	"Snowboard",
	"Snowshoe",
	"Soccer",
	"Squash",
	"StairStepper",
	"StandUpPaddling",
	"Surfing",
	"Swim",
	"TableTennis",
	"Tennis",
	"TrailRun",
	"Velomobile",
	"VirtualRide",
	"VirtualRow",
	"VirtualRun",
	"Volleyball",
	"Walk",
	"WeightTraining",
	"Wheelchair",
	"Windsurf",
	"Workout",
	"Yoga",
]


type ActivityType = Literal[
	"AlpineSki",
	"BackcountrySki",
	"Canoeing",
	"Crossfit",
	"EBikeRide",
	"Elliptical",
	"Golf",
	"Handcycle",
	"Hike",
	"IceSkate",
	"InlineSkate",
	"Kayaking",
	"Kitesurf",
	"NordicSki",
	"Ride",
	"RockClimbing",
	"RollerSki",
	"Rowing",
	"Run",
	"Sail",
	"Skateboard",
	"Snowboard",
	"Snowshoe",
	"Soccer",
	"StairStepper",
	"StandUpPaddling",
	"Surfing",
	"Swim",
	"Velomobile",
	"VirtualRide",
	"VirtualRun",
	"Walk",
	"WeightTraining",
	"Wheelchair",
	"Windsurf",
	"Workout",
	"Yoga",
]

@dataclass
class ApiActivity:
	id: int
	achievement_count: int | None
	"""
	The number of achievements gained during this activity
	"""
	athlete_id: int | None
	athlete_count: int | None
	"""
	The number of athletes for taking part in a group activity
	"""
	average_speed: float | None
	"""
	The activity's average speed, in meters per second
	"""
	average_watts: float | None
	"""
	Average power output in watts during this activity. Rides only
	"""
	comment_count: int | None
	"""
	The number of comments for this activity
	"""
	commute: bool | None
	"""
	Whether this activity is a commute
	"""
	device_name: str | None
	"""
	The name of the device used to record the activity
	"""
	device_watts: bool | None
	"""
	Whether the watts are from a power meter, false if estimated
	"""
	distance: float | None
	"""
	The activity's distance, in meters
	"""
	elapsed_time: int | None
	"""
	The activity's elapsed time, in seconds
	"""
	elev_high: float | None
	"""
	The activity's highest elevation, in meters
	"""
	elev_low: float | None
	"""
	The activity's lowest elevation, in meters
	"""
	end_lat: float | None
	end_long: float | None
	external_id: str | None
	"""
	The identifier provided at upload time
	"""
	flagged: bool | None
	"""
	Whether this activity is flagged
	"""
	gear_id: str | None
	"""
	The id of the gear for the activity
	"""
	has_kudoed: bool | None
	"""
	Whether the logged-in athlete has kudoed this activity
	"""
	hide_from_home: bool | None
	"""
	Whether the activity is muted
	"""
	kilojoules: float | None
	"""
	The total work done in kilojoules during this activity. Rides only
	"""
	kudos_count: int | None
	"""
	The number of kudos given for this activity
	"""
	manual: bool | None
	"""
	Whether this activity was created manually
	"""
	map_id: str | None
	"""
	The identifier of the map
	"""
	map_polyline: str | None
	"""
	The polyline of the map, only returned on detailed representation of an object
	"""
	map_summary_polyline: str | None
	"""
	The summary polyline of the map
	"""
	max_speed: float | None
	"""
	The activity's max speed, in meters per second
	"""
	max_watts: int | None
	"""
	Rides with power meter data only
	"""
	moving_time: int | None
	"""
	The activity's moving time, in seconds
	"""
	name: str | None
	"""
	The name of the activity
	"""
	photo_count: int | None
	"""
	The number of Instagram photos for this activity
	"""
	private: bool | None
	"""
	Whether this activity is private
	"""
	sport_type: SportType | None
	start_date: datetime | None
	"""
	The time at which the activity was started.
	"""
	start_date_local: datetime | None
	"""
	The time at which the activity was started in the local timezone.
	"""
	start_lat: float | None
	start_long: float | None
	timezone: str | None
	"""
	The timezone of the activity
	"""
	total_elevation_gain: float | None
	"""
	The activity's total elevation gain.
	"""
	total_photo_count: int | None
	"""
	The number of Instagram and Strava photos for this activity
	"""
	trainer: bool | None
	"""
	Whether this activity was recorded on a training machine
	"""
	type: ActivityType | None
	"""
	Deprecated. Prefer to use sport_type
	"""
	upload_id: int | None
	"""
	The identifier of the upload that resulted in this activity
	"""
	upload_id_str: str | None
	"""
	The unique identifier of the upload in string format
	"""
	weighted_average_watts: int | None
	"""
	Similar to Normalized Power. Rides with power meter data only
	"""
	workout_type: int | None
	"""
	The activity's workout type
	"""
	calories: float | None
	"""
	The number of kilocalories consumed during this activity
	"""
	description: str | None
	"""
	The description of the activity
	"""
	device_name: str | None
	"""
	The name of the device used to record the activity
	"""
	embed_token: str | None
	"""
	The token used to embed a Strava activity
	"""
	gear_distance: float | None
	"""
	The distance logged with this gear.
	"""
	gear_id: str | None
	"""
	The gear's unique identifier.
	"""
	gear_name: str | None
	"""
	The gear's name.
	"""
	photos_count: int | None
	photos_primary_id: int | None
	photos_urls: str | None
