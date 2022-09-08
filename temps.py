import requests
import numpy
import json
import time

i = 0
payload = []
r = requests.get('https://httpbin.org/get')

with open('temperature.txt', 'r') as malinger:
    
    
    for line in malinger:
        payload.append((100/4095)*float(line)-50)
        try: 
            payload.pop(1199)
        except:
             print('under 1200 målinger')
        print(payload[i])
        if r.status_code == 200:
            post = requests.post('https://httpbin.org/post', data=str(payload[i]))
            print(post.text)
            time.sleep(0.1)
        i+=1