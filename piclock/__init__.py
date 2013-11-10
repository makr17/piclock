from   datetime import datetime, timedelta
import httplib
import json
import os
from   suds.client import Client
from   xml.dom.minidom import parseString

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None 

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance
    

class Config:
    def __init__(self):
        # pull config from file
        f = open(os.environ['HOME']+'/clock.config.json')
        config = json.load(f)
        f.close()
        # load geoip
        geo = Geo()
        # default lat/lon/tz if not in geoip response
        if not geo.latitude:
            geo.latitude(config.get('latitude'))
        if not geo.longitude:
            geo.longitude(config.get('longitude'))
        if not geo.timezone:
            geo.timezone(config.get('timezone'))                         
        # and replace geo config with geo object
        config['geo'] = geo
        self.config = config

    def get_latitude(self):
        return self.config['geo'].latitude
    latitude  = property(get_latitude)
    def get_longitude(self):
        return self.config['geo'].longitude
    longitude = property(get_longitude)
    def get_timezone(self):
        return self.config['geo'].timezone
    timezone  = property(get_timezone)
    def get_alarms(self):
        return self.config['alarms']
    alarms = property(get_alarms)
    

class Clock:
    pass


class Geo:
    # geoip is a singleton so we only call once
    __metaclass__ = Singleton
    def __init__(self):
        conn = httplib.HTTPConnection('www.telize.com')
        conn.request('GET', '/geoip')
        res = conn.getresponse()
        body = res.read()
        geo = json.loads(body)
        self.data = geo

    def get_latitude(self):
        return self.data.get('latitude')
    def get_longitude(self):
        return self.data.get('longitude')
    def get_timezone(self):
        return self.data.get('timezone')

    latitude  = property(get_latitude)
    longitude = property(get_longitude)
    timezone  = property(get_timezone)


class Weather:
    def __init__(self, config):
        self.config = config
        wsdl = "http://graphical.weather.gov/xml/DWMLgen/wsdl/ndfdXML.wsdl"
        self.client = Client(wsdl)
        self.products = self.client.factory.create("ns0:productType")
        self.units = self.client.factory.create("ns0:unitType")
        self.formats = self.client.factory.create("ns0:formatType")
        self.highTemps = self.fetchHighTemps()

    def refresh(self):
        self.highTemps = self.fetchHighTemps()

    def fetchHighTemps(self):
        # request max temps (highs)
        params = self.client.factory.create("ns0:weatherParametersType")
        params.maxt = 1

        # pull forecast for today and tomorrow
        begin = datetime.now()
        end = begin + timedelta(days=1)

        xml = self.client.service.NDFDgen(
            self.config.latitude,
            self.config.longitude,
            self.products["glance"],
            begin,
            end,
            self.units["e"],
            params
        )
        dom = parseString(xml)
        nodes = dom.getElementsByTagName('temperature')[0].getElementsByTagName('value')
        temps = [int(x.childNodes[0].nodeValue) for x in nodes]
        return temps
