import requests
import numpy as np
import time
import datetime


targetUrl = 'https://httpbin.org/get'
backupUrl = 'https://httpbin.org/dump'
infile = 'temperature.txt'
totbits = 4096  # 12bit ADC
slpTime_reads = 0.10
intervalTime = 120  # timeinterval in sec
prev = 0


def outputer():
    launch = time.time()
    start = datetime.datetime.utcnow().isoformat()
    payload = []  # List for all the data
    # while time is less than 2 mins from start..
    while time.time() < launch+intervalTime:
        with open(infile, 'r') as measures:
            for line in measures:
                if time.time() > launch+intervalTime:
                    break
                else:
                    payload.append((100/totbits)*float(line)-50)
                    time.sleep(slpTime_reads)
                    # print(payload)
    return payload, start, datetime.datetime.utcnow().isoformat()

# The final value for return is a direct funtion in stead of variable like the "start"-one so that it is not called pre-return, hence giving
# a new value for the call

# HTTP-posting of values


def Sendres(pl, url):
    request = requests.post(url, json=pl)
    return request.status_code

# returns the min, max and avg with rounding to 2 decimals


def extraOutput(data):
    max = np.round(float(np.max(data)), 2)
    min = np.round(float(np.min(data)), 2)
    avg = np.round(float(np.mean(data)), 2)
    return max, min, avg


# prepare data for shipment in Json form
def formatforJson(max, min, avg, startTime, endTime):
    data = {
        "time": {
            "start": str(startTime),
            "end": str(endTime)
        },
        "min": min,
        "max": max,
        "avg": avg
    }
    return data

# Backup for failed sends. Holds up to 10 at a time. Pops out the first one added when full


def backup(rcv, bup):
    if(len(bup) > 9):
        bup.pop(-1)
    bup.append(rcv)
    return bup


def main():
    archive = []
    sendfail = 0
    while True:
        data, start, end = outputer()
        max, min, avg = extraOutput(data)
        tosend = formatforJson(max, min, avg, start, end)
        archive = backup(tosend, archive)

        if sendfail >= 1:
            retry = Sendres(archive[-1], targetUrl)
            print("Trying again")
            if retry != 200:
                uhoh = Sendres(archive, backupUrl)
                print("Retry failed, sending to backupserver")
            else:
                print("retry succesful!")
        post = Sendres(tosend, targetUrl)
        if post != 200:
            sendfail += 1
            print("Post error, retry on next post")
        else:
            sendfail = 0
            print("Post success!")


main()
