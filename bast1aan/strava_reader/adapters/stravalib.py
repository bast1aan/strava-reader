import os
import datetime
from pathlib import Path
import json
from typing import TypedDict, cast

import stravalib
import stravalib.protocol

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

    client = stravalib.Client(
        access_token=token_info['access_token'],
        refresh_token=token_info['refresh_token'],
        token_expires=token_info['expires_at']
    )
    activities = client.get_activities(after=datetime.datetime.now() - datetime.timedelta(days=156), limit=10)
    for activity_summary in activities:
        print(activity_summary.sport_type)

if __name__ == '__main__':
    main()
