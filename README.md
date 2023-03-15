# e-paper-meteo
Display meteo on a e-paper screen

## Devices :

- Raspberry Pi Zero WH
- Waveshare Universal e-Paper Driver Hat
- 5.83inch e-Paper HAT

![alt text](https://github.com/christophe-allemant/e-paper-meteo/blob/main/e-paper_demo.jpg?raw=true)

## Informations :

Weather is taken on openweathermap.org by using the REST API
You have to register on the website to get the appid that allow you to use the API

For the e-paper HAT, the library used is waveshare_epd in the Python part of https://github.com/waveshare/e-Paper

## Loop refresh by using cron :

*/30 * * * * launch.sh
