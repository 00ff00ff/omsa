# -*- coding: utf-8 -*-
import requests
import time



while True:
    r = requests.get('http://api.open-notify.org/iss-now.json')
    if r.text[13:20] == 'success':
        longitude = r.text[r.text.find('longitude')+13:r.text.find('", "latitude')]
        latitude = r.text[r.text.find('latitude')+12:r.text.find('"}, "timestamp')-2]
        longitude = float(longitude)
        latitude = float(latitude)
        if (longitude > -24 and longitude < -14) and (latitude > 49 and latitude < 55):
            print 'ISS Jest nad Polską'

        if ((longitude > -60 and longitude < 50) and (latitude > -60 and latitude < 40)):
            print 'ISS Jest nad danym obszarem'
        print 'Długość geograficzna: '+ str(longitude) 
        print 'Szerokość geograficzna: ' + str(latitude) +'\n'
        time.sleep(1)
