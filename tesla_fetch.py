from tesla_api import TeslaApiClient
import requests
import time
import json

previouslyActive = True
while True:
        try:
                client = TeslaApiClient('user@email.com', 'yourteslapassword')
                vehicles = client.list_vehicles()
                v = vehicles[0]
                state = v.state
                if (state == 'asleep'):
                        print("Asleep. Waiting for 5 minutes...")
                        previouslyActive = False
                        time.sleep(5*60)
                else:
                        print("getting data...")
                        drive_state = v.get_drive_state()
                        charge = v.charge.get_state()
                        #print(charge)
                        print(drive_state)
                        speed = drive_state['speed']
                        shift_state = drive_state['shift_state']
                        if (speed == None):
                            speed = 0.0
                        else:
                            speed = float(speed) * 1.60934 # convert to km/h
                        payload = {}
                        payload.update(timestamp = int(round(time.time() * 1000)))
                        location = {}
                        location.update(lat = drive_state['latitude'])
                        location.update(lon = drive_state['longitude'])
                        payload.update(location = location)
                        payload.update(soc = charge['usable_battery_level'])
                        payload.update(speed = speed)
                        print(json.dumps(payload))
                        #v.controls.flash_lights()
                        headers = {"Content-Type" : "application/json"}
                        r = requests.post("http://127.0.0.1:9200/tesla/tesla", headers = headers, data = json.dumps(payload))
                        #print(r.content)
                        if (shift_state == None and previouslyActive == True):
                                print("Shift state switched to none, sleeping for 21 minutes...")
                                time.sleep(21*60)
                        else:
                                previouslyActive = True;
                                print("Driving, sleeping for 30 seconds...")
                                time.sleep(30)
        except:
                print("An exception occured!")
                time.sleep(120);
