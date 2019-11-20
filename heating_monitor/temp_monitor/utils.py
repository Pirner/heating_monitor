import os

from . import models
from heating_monitor import settings


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

        sensor_file = os.path.join('/','sys', 'bus', 'w1', 'devices', sensor.name, 'w1_slave')
        f = open(sensor_file, 'r')
        lines = f.readlines()
        f.close()
        set_trace()
        temp_str = lines[1].find('t=')
        temp_cels = 0
        # check if temperature was written
        if temp_str != -1 :
            temp_data = lines[1][temp_str+2:]
            temp_cels = float(temp_data) / 1000.0
        print('temperature is: ', temp_cels)
