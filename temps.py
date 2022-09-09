import requests
import numpy
import json
import time



payload = []
backup=[]
listSpaces = 120/0.1 - 1


r = requests.get('https://httpbin.org/get')#just to make sure there is contact




def getTemperature():
    i = 0
    with open('temperature.txt', 'r') as malinger:
        for line in malinger:
            time.sleep(0.1)
            payload.append((100/4095)*float(line)-50)#quick and dirty way to get temperatures.
            if i >= listSpaces:#make sure the list remains at 2 mins. Min, Max and avg only need an update at 2min intervals
                avgTemp = numpy.mean(payload)
                payload.clear()
                print("Cleared")
                i = 0
            else:
                maxlist = max(payload)
                minlist = min(payload)
                print(numpy.mean(payload), maxlist, minlist)
                i+=1

getTemperature()

#if r.status_code == 200:
#    post = requests.post('https://httpbin.org/post', data=str(payload[i]))
#    print(post.text)
#    time.sleep(0.1)
#elif r.status_code == 500:
#    post = requests.post('https://httpbin.org/dump', data=str(payload[i]))