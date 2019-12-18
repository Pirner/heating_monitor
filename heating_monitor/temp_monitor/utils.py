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
    check_log_directory()
    sensors = models.TempSensor.objects.all()
    for sensor in sensors:
        try:
            sensor_file = os.path.join('/','sys', 'bus', 'w1', 'devices', sensor.hw_id, 'w1_slave')
            f = open(sensor_file, 'r')
            lines = f.readlines()
            f.close()
            temp_str = lines[1].find('t=')
            temp_cels = 0
            # check if temperature was written
            if temp_str != -1 :
                temp_data = lines[1][temp_str+2:]
                temp_cels = float(temp_data) / 1000.0
                sensor.last_temperature = temp_cels
                sensor.save()
            else:
                sensor.last_temperature = -1.0
                sensor.save()
            print('temperature is: ', temp_cels)
        except Exception as e:
            sensor.last_temperature = -1.0
            sensor.save()
            print(e)
