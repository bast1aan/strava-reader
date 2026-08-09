import pickle
import unittest
from typing import cast

from stravalib.strava_model import DetailedActivity

from bast1aan.strava_reader.adapters.stravalib import _pydantic_to_entity


class ConvertPydanticToEntityTestCase(unittest.TestCase):

    def test(self) -> None:
        with open('activity.pickle', 'rb') as f:
            activity = cast(DetailedActivity, pickle.loads(f.read()))
        api_activity = _pydantic_to_entity(activity)

        self.fail(api_activity)
