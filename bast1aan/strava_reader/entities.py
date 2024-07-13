from dataclasses import dataclass
from datetime import datetime, timedelta


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
