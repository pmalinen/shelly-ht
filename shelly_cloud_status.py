#!/usr/bin/env python3
import http.client
import json
import configparser
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

configfile = '.shellyrc'


def get_config(section):
    config = configparser.ConfigParser()
    config.read(configfile)

    token = config[section]['token']
    url = config[section]['server']

    if section == "shelly":
        devices = config[section]['devices']
        return url, token, devices
    else:
        org = config[section]['org']
        bucket = config[section]['bucket']
        return url, token, org, bucket


def request_data(key, device_id, url):
    conn = http.client.HTTPSConnection(url)
    payload = "auth_key="+key+"&"+"id="+device_id
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }
    conn.request("POST", "/device/status", payload, headers)
    res = conn.getresponse()
    data = res.read().decode('utf-8')
    return data


def write_data(alias, name, value):
    url, token, org, bucket = get_config("influx")
    # print(url, token, org)
    client = InfluxDBClient(url=url, token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    if alias == "temp":
        p = Point("event").tag("hostname", name).field("temperature", value)
    elif alias == "humidity":
        p = Point("event").tag("hostname", name).field("humidity", value)
    write_api.write(bucket=bucket, org=org, record=p)
    print(name, value, bucket)


def main():
    # get config for shelly
    url, token, devices = get_config("shelly")
    devices = devices.split(",")

    # Go through devices and get relevant fields
    for device_id in devices:
        data = request_data(token, device_id, url)
        json_obj = json.loads(data)
        name = (json_obj['data']['device_status']['getinfo']['tz_info']['device'])
        hum = (json_obj['data']['device_status']['hum']['value'])
        tmp = (json_obj['data']['device_status']['tmp']['value'])

        # Write data to influxdb
        write_data("temp", name, tmp)
        write_data("humidity", name, hum)


if __name__ == "__main__":
    main()
