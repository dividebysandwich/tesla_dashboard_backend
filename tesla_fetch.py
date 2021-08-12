import teslapy
import requests
import time
import json

previouslyActive = True
while True:
        try:
#            def solve_captcha(svg):
#                with open('captcha.svg', 'wb') as f:
#                    f.write(svg)
#                return input('Captcha: ')
            with teslapy.Tesla('yourname@email.com', 'supersecretpassword', None, None, None, None, None, 0, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36") as tesla:
#                tesla.captcha_solver = solve_captcha
                tesla.fetch_token()
                vehicles = tesla.vehicle_list()
                v = vehicles[0]
                vehicle_data = v.get_vehicle_data()
                state = vehicle_data['state']
                if (state == 'asleep'):
                        print("Asleep. Waiting for 5 minutes...")
                        previouslyActive = False
                        time.sleep(5*60)
                else:
                        print("getting data...")
                        drive_state = vehicle_data['drive_state']
                        charge = vehicle_data['charge_state']['battery_level']
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
                        r = requests.post("http://elasticsearch:9200/tesla/tesla", headers = headers, data = json.dumps(payload))
                        #print(r.content)
                        if (shift_state == None and previouslyActive == True):
                                print("Shift state switched to none, sleeping for 21 minutes...")
                                time.sleep(21*60)
                        else:
                                previouslyActive = True;
                                print("Driving, sleeping for 30 seconds...")
                                time.sleep(30)
        except Exception as e:
                print(e)
                time.sleep(120);
