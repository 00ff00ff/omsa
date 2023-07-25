import requests
from picamera import PiCamera
from fractions import Fraction
import time

camera = PiCamera(
    resolution=(1280, 720),
    framerate=Fraction(1, 6),
    sensor_mode=3)
camera.shutter_speed = 6000000
camera.iso = 800
camera.exposure_mode = 'off'
camera.start_preview()
time.sleep(10)

frame = 0
x = 1
interval = 60
r_sunset = requests.get('http://api.sunrise-sunset.org/json?lat= 53.4837486&lng=18.753565&date=today')
r_sunrise = requests.get('http://api.sunrise-sunset.org/json?lat= 53.4837486&lng=18.753565&date=tomorrow')
print r_sunset.text

def Sunrise():
    p = r_sunrise.text.find('sunrise')
    pos = r_sunrise.text.find('AM')
    sunrise = r_sunrise.text[p+10:pos-4]
   # sunrise = '3:30'
    current_time = time.strftime('%I:%M')
    current_time = current_time[1:5]
    if current_time == sunrise:
        return True
    else:
        return False

    

def Sunset():
    p = r_sunset.text.find('sunset')
    pos = r_sunset.text.find('PM')
    sunrise = r_sunset.text[p+9:pos-4]
   # sunrise = '11:30'
    current_time = time.strftime('%I:%M')
    if current_time == sunrise:
        return True
    else:
        return False

def Capture():
    global frame
    while Sunrise() == False:
        camera.capture('image%s.jpg' % frame)
        frame += 1
        time.sleep(interval)

while x == 1:
    global x
    if Sunset() == True:
        
        Capture()
        x = 0
    time.sleep(interval)

FinalImage = Image('image%s.jpg' % frame) - Image('image%s.jpg' % frame)

while x < frame:
    first = Image('image%s.jpg' % x)
    if x == pictures:
        second = Image('image%s.jpg' % x)
    else:
        frame += 1
        second = Image('image%s.jpg' % x)
    diff = second - first
    diff = diff.binarize(15)
    diff = diff.invert()
    FinalImage += diff
    x += 1

current_time = strftime('%H:%M:%S')
current_date = strftime('%d-%m-%Y')
FinalImage.save('picture'+current_date+' '+current_time+'.jpg')
camera.stop_preview()
        
        
