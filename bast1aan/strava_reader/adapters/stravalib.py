import dataclasses
import os
import datetime
import pickle
from pathlib import Path
import json
from typing import cast, Iterator

import stravalib
import stravalib.protocol
from stravalib import strava_model

from bast1aan.strava_reader.entities import ApiActivity

client_id = int(os.environ['STRAVA_CLIENT_ID'])
client_secret = os.environ['STRAVA_CLIENT_SECRET']

access_info_dir = Path(os.environ['XDG_RUNTIME_DIR'])

redirect_uri = 'http://localhost/strava-reader/callback'
scope: list[stravalib.protocol.Scope] = ['read', 'read_all', 'profile:read_all', 'activity:read', 'activity:read_all']

def _validate[T](t: type[T], obj: dict) -> T:
    for key in getattr(t, '__required_keys__', ()):
        if key not in obj:
            raise TypeError(f"{key} not in {obj}")
    return cast(T, obj)

def _store_access_info(access_info: stravalib.protocol.AccessInfo) -> None:
    with open(access_info_dir / 'stravalib_access_info.json', 'w') as f:
        json.dump(access_info, f)

def _get_stored_access_info() -> stravalib.protocol.AccessInfo | None:
    try:
        with open(access_info_dir / 'stravalib_access_info.json', 'r') as f:
            access_info = json.load(f)
            return _validate(stravalib.protocol.AccessInfo, access_info)
    except Exception:
        return None

def main() -> None:
    token_info = _get_stored_access_info()
    if not token_info:
        client = stravalib.Client()
        authorization_url = client.authorization_url(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
        )
        print(f'Please go to {authorization_url} and authorize access.')
        code = input('Enter the code: ')
        token_info = cast(
            stravalib.protocol.AccessInfo,
            client.exchange_code_for_token(
                client_id=client_id, client_secret=client_secret, code=code
            )
        )
        _store_access_info(token_info)

    # client = stravalib.Client(
    #     access_token=token_info['access_token'],
    #     refresh_token=token_info['refresh_token'],
    #     token_expires=token_info['expires_at']
    # )
    # activities = client.get_activities(after=datetime.datetime.now() - datetime.timedelta(days=156), limit=10)
    # activity = client.get_activity(activity_id=cast(int, next(activities).id))
    # with open('activity.pickle', 'wb') as f:
    #     f.write(pickle.dumps(activity))
    # print(repr(activity))

    #for activity_summary in activities:
    #    print(activity_summary.sport_type)

if __name__ == '__main__':
    main()


def get_activities(after: int) -> Iterator[ApiActivity]:
    token_info = _get_stored_access_info()
    if not token_info:
        raise RuntimeError('Not logged in')
    client = stravalib.Client(
        access_token=token_info['access_token'],
        refresh_token=token_info['refresh_token'],
        token_expires=token_info['expires_at']
    )
    after_td = datetime.datetime.fromtimestamp(after)
    while(True):
        activity = None
        activities = client.get_activities(after=after_td, limit=25)
        for summary_act in activities:
            activity = client.get_activity(activity_id=cast(int, summary_act.id))
            yield _pydantic_to_entity(activity)
        if not activity:
            break
        after_td = activity.start_date
        if after_td is None:
            break


def _pydantic_to_entity(da: stravalib.strava_model.DetailedActivity) -> ApiActivity:
    special_fields = {
        'map_polyline': lambda: da.map.polyline,
        'map_summary_polyline': lambda: da.map.summary_polyline,
        'start_lat': lambda: da.start_latlng[0],
        'start_long': lambda: da.start_latlng[1],
        'photos_count': lambda: da.photos.count,
        'photos_primary_id': lambda: da.photos.primary.id,
        'photos_urls': lambda: json.dumps(da.photos.primary.urls),
        'gear_distance': lambda: da.gear.distance,
        'gear_name': lambda: da.gear.name,
        'map_id': lambda: da.map.id,
        'end_lat': lambda: da.end_latlng[0],
        'end_long': lambda: da.end_latlng[1],
        'athlete_id': lambda: da.athlete.id,
        'sport_type': lambda: da.sport_type.root,
        'type': lambda: da.type.root,


    }

    all_fields = {field.name for field in dataclasses.fields(ApiActivity)}

    special_fields_values = {}
    for name, get_value in special_fields.items():
        try:
            special_fields_values[name] = get_value()
        except Exception:
            special_fields_values[name] = None

    activity = ApiActivity(
        **{field: getattr(da, field) for field in all_fields - special_fields.keys()},
        **special_fields_values
    )
    return activity
