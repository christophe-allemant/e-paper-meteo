#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
import traceback
import requests
import json
import datetime

from datetime import datetime
from waveshare_epd import epd5in83
from PIL import Image,ImageDraw,ImageFont

city = "Nantes"
appid = "" #Get your ID on https://openweathermap.org/
pos_lon = "-1.529049"
pos_lat = "47.1942589"
today = datetime.now()

#######
# For the list of differents weather of the API : https://openweathermap.org/weather-conditions
#######
url_weather = "http://api.openweathermap.org/data/2.5/weather?lon="+pos_lon+"&lat="+pos_lat+"&APPID="+appid
url_forecast = "http://api.openweathermap.org/data/2.5/forecast?q="+city+"&lang=fr&APPID="+appid
url_onecall = "http://api.openweathermap.org/data/2.5/onecall?lon="+pos_lon+"&lat="+pos_lat+"&APPID="+appid

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Display Meteo")

    ########################
    # Get forecast weather #
    ########################
    r_forecast = requests.get(url_forecast)
    data = r_forecast.json()
    liste_temps = [];
    nb = 0;
    for i in range (0,25): #8 by day
        t = data['list'][i]['main']['temp']
        f = data['list'][i]['main']['feels_like']
        pres = data['list'][i]['main']['pressure']
        humid = data['list'][i]['main']['humidity']
        temps = data['list'][i]['weather'][0]['main']
        descr = data['list'][i]['weather'][0]['description']
        wind = data['list'][i]['wind']['speed']
        wind_angle = data['list'][i]['wind']['deg']

        time = datetime.fromtimestamp(data['list'][i]['dt'])

        tab_temps = [];
        tab_temps.append(time);
        tab_temps.append(format(round(t-273.15)))
        tab_temps.append(format(temps))
        tab_temps.append(format(descr))
        tab_temps.append(format(pres))
        tab_temps.append(format(humid))
        tab_temps.append(format(round(f-273.15)))
        tab_temps.append(format(round(wind * (18/5),2)))
        tab_temps.append(format(wind_angle))
        liste_temps.append(tab_temps)
        nb=nb+1

    #################
    # PRINTING TIME #
    #################
    epd = epd5in83.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font32 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
    font72 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 72)

    logging.info("4.read bmps file on window")
    Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage2)
    draw.rectangle((0,0,epd.width, epd.height), fill=0, outline=0)

    draw.rectangle((15, 15, 585, 60), fill="#ffffff", outline="#ffffff")
    date_text = (str(today.day) if(today.day>=10) else "0"+str(today.day)) + "/" + (str(today.month) if(today.month>=10) else "0"+str(today.month)) + "/" + str(today.year)
    draw.text((220, 20), date_text, font = font32, fill = 0)

    draw.rectangle((15, 75, 195, 433), fill="#ffffff", outline="#ffffff")
    draw.rectangle((210, 75, 390, 433), fill="#ffffff", outline="#ffffff")
    draw.rectangle((405, 75, 585, 433), fill="#ffffff", outline="#ffffff")

    ################
    # GET PIC NAME #
    ################
    def getPicName(str, des):
        if (str == "Clouds" and des.find("nuageux") != -1):
            return "nuageux.bmp"
        if (str == "Clouds"):
            return "couvert.bmp"
        if (str == "Rain"):
            return "pluie.bmp"
        if (str == "Clear"):
            return "soleil.bmp"
        if (str == "Snow"):
            return "neige.bmp"
        if (str == "Drizzle"):
            return "couvert.bmp"
        if (str == "Thunderstorm"):
            return "orage.bmp"
        return "error.bmp"

    #################
    # DISPLAY METEO #
    #################
    img1 = Image.open(os.path.join(picdir, getPicName(liste_temps[0][2],liste_temps[0][3])))
    img2 = Image.open(os.path.join(picdir, getPicName(liste_temps[1][2],liste_temps[1][3])))
    img3 = Image.open(os.path.join(picdir, getPicName(liste_temps[2][2],liste_temps[2][3])))

    draw.text((85, 75), (str(liste_temps[0][0].hour) if(liste_temps[0][0].hour>=10) else "0"+str(liste_temps[0][0].hour))+":"+(str(liste_temps[0][0].minute) if(liste_temps[0][0].minute>=10) else "0"+str(liste_temps[0][0].minute)), font = font18, fill = 0)
    draw.text((280, 75), (str(liste_temps[1][0].hour) if(liste_temps[1][0].hour>=10) else "0"+str(liste_temps[1][0].hour))+":"+(str(liste_temps[1][0].minute) if(liste_temps[1][0].minute>=10) else "0"+str(liste_temps[1][0].minute)), font = font18, fill = 0)
    draw.text((475, 75), (str(liste_temps[2][0].hour) if(liste_temps[2][0].hour>=10) else "0"+str(liste_temps[2][0].hour))+":"+(str(liste_temps[2][0].minute) if(liste_temps[2][0].minute>=10) else "0"+str(liste_temps[2][0].minute)), font = font18, fill = 0)

    Himage2.paste(img1, (15,105))
    Himage2.paste(img2, (210,105))
    Himage2.paste(img3, (405,105))

    draw.text((20, 270), liste_temps[0][1]+"°C", font = font72, fill = 0)
    draw.text((215, 270), liste_temps[1][1]+"°C", font = font72, fill = 0)
    draw.text((410, 270), liste_temps[2][1]+"°C", font = font72, fill = 0)

    draw.text((20, 350), "Ressenti : "+liste_temps[0][6]+"°C", font = font18, fill = 0)
    draw.text((215, 350), "Ressenti : "+liste_temps[1][6]+"°C", font = font18, fill = 0)
    draw.text((410, 350), "Ressenti : "+liste_temps[2][6]+"°C", font = font18, fill = 0)

    draw.text((20, 370), "Vent : "+liste_temps[0][7]+" km/h", font = font18, fill = 0)
    draw.text((215, 370), "Vent : "+liste_temps[1][7]+" km/h", font = font18, fill = 0)
    draw.text((410, 370), "Vent : "+liste_temps[2][7]+" km/h", font = font18, fill = 0)

    draw.text((20, 390), "Pression : "+liste_temps[0][4]+" hPa", font = font18, fill = 0)
    draw.text((215, 390), "Pression : "+liste_temps[1][4]+" hPa", font = font18, fill = 0)
    draw.text((410, 390), "Pression : "+liste_temps[2][4]+" hPa", font = font18, fill = 0)

    draw.text((20, 410), "Humid : "+liste_temps[0][5]+"%", font = font18, fill = 0)
    draw.text((215, 410), "Humid : "+liste_temps[1][5]+"%", font = font18, fill = 0)
    draw.text((410, 410), "Humid : "+liste_temps[0][5]+"%", font = font18, fill = 0)

    epd.display(epd.getbuffer(Himage2))

    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd5in83.epdconfig.module_exit()
    exit()
