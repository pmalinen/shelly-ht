### Shelly H&T stats

![Shelly H&T](https://shelly.cloud/wp-content/uploads/2019/07/Shelly-ht_white_black_usb.png)

**Example Dashboard**

Graphing data from Shelly H&T WiFi humidity and temperature devices on InfluxDB  and write to a InfluxDB in InfluxDB Cloud.

![Shelly H&T grafana](grafana-influx-shelly-ht.png "Grafana")

**References**

Shelly H&T:  
https://shelly.cloud/shelly-humidity-and-temperature/

APi Docs:  
https://shelly-api-docs.shelly.cloud/#shelly-h-amp-t

InfluxDB Cloud:  
https://www.influxdata.com/products/influxdb-cloud/

**Config file**

```python
[shelly]  
token = <Shelly API Token>  
devices = <comma separated list of device ids>  
server = <shelly api server>  
[influx]  
server = <influx server>  
token = <influx api token>  
org = <org name>  
bucket = <bucket name>  
```
