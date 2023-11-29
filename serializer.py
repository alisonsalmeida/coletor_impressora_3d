from json import JSONEncoder
from datetime import datetime, time, date, timedelta
import json


class Serialize(JSONEncoder):

    def default(self, field):
        if isinstance(field, datetime) or isinstance(field, time) or isinstance(field, date):
            if isinstance(field, datetime):
                return field.replace(microsecond=0).isoformat() + 'Z'

            if isinstance(field, time):
                return field.replace(microsecond=0).isoformat()

            return field.isoformat()

        if isinstance(field, timedelta):
            return field.__str__()

        return JSONEncoder.default(self, field)


class Json:
    @staticmethod
    def dumps(*args, **kwargs):
        if 'cls' not in kwargs:
            kwargs['cls'] = Serialize

        return json.dumps(*args, **kwargs)

    @staticmethod
    def loads(*args, **kwargs):
        return json.loads(*args, **kwargs)
