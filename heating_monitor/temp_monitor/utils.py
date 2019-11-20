import os

from heating_monitor.temp_monitor import models
from heating_monitor.heating_monitor import settings


def check_log_directory():
    if not os.path.isdir(settings.TEMP_LOG_FILE_LOCATION):
        try:
            os.mkdir(settings.TEMP_LOG_FILE_LOCATION)
        except OSError:
            print("Creation of the directory %s failed" % settings.TEMP_LOG_FILE_LOCATION)
            return False
        else:
            print("Successfully created the directory %s " % settings.TEMP_LOG_FILE_LOCATION)
    return True


def write_temps_to_logs():
    sensors = models.TempSensor.objects.all()
    from pudb import set_trace
    for sensor in sensors:

        sensor_file = os.path.join('sys', 'bus', 'w1', 'devices', sensor.name, 'w1_slave')
        f = open(sensor_file, 'r')
        lines = f.readlines()
        f.close()
        set_trace()