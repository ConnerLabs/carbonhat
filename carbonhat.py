''' Display carbon intensity on Sense HAT
Steve Conner, May 2021
This is only possible thanks to
api.carbonintensity.org.uk
:-)
'''

import requests
import json
import time
import datetime
from sense_hat import SenseHat

api='https://api.carbonintensity.org.uk'
postcode='G11'

'''
debug function for dumping data structure to file if needed
'''
def dump(spew):
    f=open('spew.json', 'w')
    json.dump(spew, f, indent=4)
    f.close()

'''
Get carbon intensity forecast as JSON
'''
def get_carbon_forecast():
    # Note, API wants time in UTC.
    start_time=str(datetime.datetime.utcnow().isoformat())

    r=requests.get(api+'/regional/intensity/'+start_time+'Z/fw24h/postcode/'+postcode)
    r.raise_for_status() # Throw an exception if the API call failed.

    return r.json()

'''
Crunch the JSON to a single intensity number for the next 3 hours 
'''
def crunch_forecast(f):
    intensities = []
    
    # Print the start time of the first period for test/debug purposes.
    print('Forecast starts from '+str(f['data']['data'][0]['from']))
    
    # Take 6 half hour periods
    for period in range(6):
        intensities.append(f['data']['data'][period]['intensity']['forecast'])

    avg_intensity = sum(intensities)/6.0
    print('Calculating average for next 3 hours: '+str(intensities)+' -> '+str(avg_intensity))

    return avg_intensity

'''
Convert carbon intensity to a RGB colour
'''
def carbon_to_rgb(c):

    # anything greater or equal than this will be pure red
    max_intensity=215

    if c > max_intensity:
        c = max_intensity

    if c < 0:
        c = 0

    r = int(255 * (c/max_intensity))
    g = int(255 * 1.0-(c/max_intensity))
    b = 0

    print('carbon to RGB: '+str((r,g,b)))

    return (r, g, b)

'''
Generate an array of pixels that shows :(
to indicate an error
'''
def sad_face():
    X = (255, 0, 0)
    O = (0, 0, 0)

    sad_face = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, X, O, O, X, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, X, O, O, X, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O
    ]

    return sad_face


'''
Generate an array of pixels that shows :)
'''
def happy_face():
    X = (0, 255, 0)
    O = (0, 0, 0)

    happy_face = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, X, O, O, X, O, O,
    O, O, O, O, O, O, O, O,
    O, O, X, O, O, X, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O
    ]

    return happy_face

'''
Linear interpolation to make display fade smoothly
'''
def fade(new, old, a):
    if a < 0.0:
        a = 0.0

    if a > 1.0:
        a = 1.0

    return ((new * a) + (old * (1.0-a)))

if __name__ == "__main__":
    sh = SenseHat()
    mins_since_last_check = 999
    new_intensity = -1.0

    sh.set_pixels(happy_face())

    while True:
        # Only query the API every half hour, as the results are only
        # updated every half hour, it would just waste their bandwidth.
        # Todo: Randomise the delay after the half hour if this ever gets rolled
        # out in production, so the units don't all hit the API at once
        current_time=datetime.datetime.now()
        if (current_time.minute in [1, 2, 31, 32] and mins_since_last_check > 1) or mins_since_last_check > 35:
            try:
                print('Getting carbon forecast...')
                last_intensity = new_intensity
                new_intensity = crunch_forecast(get_carbon_forecast())

                # The first time the loop runs, make last_intensity and new_intensity
                # the same, so the display starts off at the right value
                if last_intensity < 0:
                    last_intensity = new_intensity

                print('New intensity '+str(new_intensity)+', last intensity '+str(last_intensity))
                mins_since_last_check = 0

                # Dim the LEDs at night
                if current_time.hour in [23, 0, 1, 2, 3, 4, 5]:
                    sh.low_light = True

                else:
                    sh.low_light = False

            except Exception as e:
                # Something went wrong...
                sh.set_pixels(sad_face())
                raise(e)
                exit()

        else:
            mins_since_last_check = mins_since_last_check + 1

        # Update the display every minute so it fades smoothly.
        f = fade(new_intensity, last_intensity, (mins_since_last_check/30))
        print('Interpolated intensity '+str(f))
        colour=carbon_to_rgb(f)
        sh.clear(colour)

        # sleep for a minute
        time.sleep(60)
