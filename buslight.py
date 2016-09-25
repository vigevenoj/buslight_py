#!/usr/bin/env python
"""
Basic script to create an empty python package containing one module
"""
import sys
import yaml
import requests
from datetime import datetime, timedelta
import time
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.schedulers.blocking import BlockingScheduler


class BusLight():
    """
    Create an empty module with its etup script and a README file.
    """
    def __init__(self, config='./trimet.yaml'):
        try:
            with open(config, 'r') as fptr:
                configs = yaml.load(fptr.read())
                self.appID = configs['trimet']['api_key']
                self.stops = map(str, configs['trimet']['stops'])
#                self.stopID = configs['trimet']['stopID']
        except IOError as e:
            print("Unable to load configuration. {0}".format(e))
            sys.exit(1)
        self.scheduler = BackgroundScheduler()
        # self.scheduler = BlockingScheduler()
        self.scheduler.start()
        # Start phue class as well

    def schedule_next_check(self, time_to_check):
        self.scheduler.add_job(self.check_for_bus, 'date', run_date=time_to_check)
        pass

    def check_for_bus(self):
        url = "https://developer.trimet.org/ws/v2/arrivals?json=true&appID={0}&locIDs={1}"
        #url = url.format(self.appID, self.stopID)
        url = url.format(self.appID, ','.join(self.stops))
        #print(self.stops)
        #print( ','.join(self.stops))
        print(url)
        try:
            data = requests.get(url)
        except Exception as e:
            print('Unable to request from url "{0}" because {1}'.format(url, e))
            sys.exit(1)
        if data.status_code / 100 != 2:
            print('{0} response: "{1}"'.format(data.status_code, data.text))
        trimet_response = data.json()
        next_arrival = trimet_response['resultSet']['arrival'][0]
        if 'scheduled' in next_arrival:
            scheduled = next_arrival['scheduled']
        else:
            scheduled = None
        if 'estimated' in next_arrival:
            estimated = next_arrival['estimated']
        else:
            estimated = float('inf')

        soonest = min(scheduled, estimated)
        now = int(datetime.now().strftime("%s")) * 1000
        print("Currently {0}. Next bus at {1}".format(now, soonest))
        if(soonest - now >= 0):
            try:
                self.update_status(soonest - now)
            except Exception as e:
                print("Had problem updating {0}. Next check in 60s".format(e))
                self.schedule_next_check(now + timedelta(seconds=60))
        else:
            print("Negative interval, schedule next check in 60s")
            self.schedule_next_check(now + timedelta(seconds=60))

    def update_status(self, soonest_bus):
        print("we would update the lamp light and such now")
        if soonest_bus >= (15*60*1000):
            print("Light off! No bus for at least 15 minutes")
            self.schedule_next_check(datetime.now() + timedelta(minutes=5))
        elif soonest_bus >= (10 * 60 * 1000):
            print("Yellow (next bus in 10-15 minutes)")
            self.schedule_next_check(datetime.now() + timedelta(seconds=60))
        elif soonest_bus >= (9*60*1000):
            print("Gold (next bus in 9-10 minutes)")
            self.schedule_next_check(datetime.now() + timedelta(seconds=60))
        elif soonest_bus >= (7*60*1000):
            print("Goldenrod (next bus in 7-9 minutes)")
            self.schedule_next_check(datetime.now() + timedelta(seconds=60))
        elif soonest_bus >= (5*60*1000):
            print("Dark orange (next bus in 5-7 minutes)")
            self.schedule_next_check(datetime.now() + timedelta(seconds=60))
        elif soonest_bus >= (4*60*1000):
            print("Orange (next bus in 4-5 minutes)")
            self.schedule_next_check(datetime.now() + timedelta(seconds=60))
        elif soonest_bus >= (3*60*1000):
            print("Orange red (next bus in 3-4 minutes)")
            self.schedule_next_check(datetime.now() + timedelta(seconds=60))
        elif soonest_bus < (3*60*1000):
            print("Red (next bus in less than 3 minutes)")
            self.schedule_next_check(datetime.now() + timedelta(seconds=60))

if __name__ == '__main__':
    buslight = BusLight()
    buslight.check_for_bus()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        buslight.scheduler.shutdown()
