from flask_restful import Resource, reqparse
from time import time
from .lib import getWindowsForDevice
import json

DEFAULT_WINDOW_TIME = 60
DEFAULT_NUM_WINDOWS = 10
class WindowRetriever(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('device_uuid', type=str)
        parser.add_argument('end_time', type=int, default=time())
        parser.add_argument('window_time', type=int, default=DEFAULT_WINDOW_TIME)
        parser.add_argument('num_windows', type=int, default=DEFAULT_NUM_WINDOWS)
        args = parser.parse_args()
        device_uuid = args['device_uuid']
        end_time = int(args['end_time'])
        window_time = args['window_time']
        num_windows = args['num_windows']
        windows = getWindowsForDevice(device_uuid, end_time, window_time, num_windows)
        # res = json.dumps({'data': windows})
        # return res
        return {'data': windows}
