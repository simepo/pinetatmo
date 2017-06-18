from papirus import PapirusTextPos
import lnetatmo
import time, datetime
import json
import pyowm

owm_key = 'b65fbb6ad3cd36e9158f5a801683ffd8'
owm_location = 'Saffron Walden,uk'
font = '/home/pi/PaPiRus/fonts/OpenSans-Semibold.ttf'
arrow_font = '/home/pi/PaPiRus/fonts/Arrows.ttf'

while True:
    try:
        netatmo_authorization = lnetatmo.ClientAuth()
        owm = pyowm.OWM(owm_key)
        break
    except:
        print 'Unable to connect to Internet, waiting 30 seconds and retrying'
        time.sleep(30)

while True:
    now = time.strftime("%Y-%m-%d %H:%M")
    
    screen = PapirusTextPos(False)
    
    try:
        weatherData = lnetatmo.WeatherStationData(netatmo_authorization)
        latest_data = weatherData.lastData()
        forecast = owm.daily_forecast(owm_location, limit=2)
    except:
        print 'Unable to update data, skipping'
        pass

    data_time = datetime.datetime.fromtimestamp(latest_data['Outdoor']['When']).strftime('%Y-%m-%d %H:%M')
    out_temp = '{: 6.1f}'.format(latest_data['Outdoor']['Temperature'])
    bedroom_temp = '{: 6.1f}'.format(latest_data['Indoor']['Temperature'])
    out_humidity = latest_data['Outdoor']['Humidity']
    if latest_data['Outdoor']['temp_trend'] == 'up':
        trend_symbol = 'c'
    elif latest_data['Outdoor']['temp_trend'] == 'down':
        trend_symbol = 'd'
    else:
        trend_symbol = 'a'
    
    if datetime.datetime.now().hour > 15:
        forecast_day = 1
        forecast_title = "Tomorrow"
    else:
        forecast_day = 0
        forecast_title = "Today"
    forecast_details = forecast.get_forecast()
    forecast_details_list = forecast_details.get_weathers()
    forecast_high = '{: 6.1f}'.format(forecast_details_list[forecast_day].get_temperature(unit='celsius')['max'])
    forecast_text = forecast_details_list[forecast_day].get_status()

    screen.AddText('Outdoor', 5, 3, 20, Id='OutTitle', font_path=font)
    screen.AddText(out_temp + u"\u00b0", 5, 10, 70, Id="OutTemp", font_path=font)
    screen.AddText(trend_symbol, 170, 30, 50, font_path=arrow_font)
    screen.AddText('Humidity ' + str(out_humidity) + '%', 5, 86, 12, Id='Humidity', font_path=font)
    screen.AddText('Bedroom', 5, 103, 15, Id='InTitle', font_path=font)
    screen.AddText(bedroom_temp + u"\u00b0", 5, 115, 35, Id='InTemp', font_path=font)
    screen.AddText(forecast_title, 130, 93, 15, Id='FcTitle', font_path=font)
    screen.AddText(forecast_high + u"\u00b0", 130, 105, 35, Id='FcTemp', font_path=font)
    screen.AddText(forecast_text, 130, 143, 12, Id='FcText', font_path=font)
    screen.AddText(data_time, 10, 164, 10, Id='When', font_path=font)
    screen.WriteAll()

    print "Updated at " + now + " with data timed " + data_time

    time.sleep(600)
