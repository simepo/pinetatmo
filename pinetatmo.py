from papirus import PapirusTextPos
import lnetatmo
import time, datetime
import json

font = '/home/pi/PaPiRus/fonts/OpenSans-Semibold.ttf'
arrow_font = '/home/pi/PaPiRus/fonts/Arrows.ttf'

authorization = lnetatmo.ClientAuth()

while True:
    screen = PapirusTextPos(False)
    weatherData = lnetatmo.WeatherStationData(authorization)
    latest_data = weatherData.lastData()
    now = time.strftime("%Y-%m-%d %H:%M")
    data_time = datetime.datetime.fromtimestamp(latest_data['Outdoor']['When']).strftime('%Y-%m-%d %H:%M')
    out_temp = '{: 6.1f}'.format(latest_data['Outdoor']['Temperature'])
    out_humidity = latest_data['Outdoor']['Humidity']
    # out_temp = '{: 6.1f}'.format(-13.2)

    if latest_data['Outdoor']['temp_trend'] == 'up':
        trend_symbol = 'c'
    elif latest_data['Outdoor']['temp_trend'] == 'down':
        trend_symbol = 'd'
    else:
        trend_symbol = 'a'
    
    screen.AddText('Outdoor', 5, 3, 20, Id='Title', font_path=font)
    screen.AddText(out_temp + u"\u00b0", 5, 10, 70, Id="OutTemp", font_path=font)
    screen.AddText(trend_symbol, 170, 30, 50, font_path=arrow_font)
    screen.AddText('Humidity ' + str(out_humidity) + '%', 5, 86, 15, Id='Humidity', font_path=font)
    screen.AddText(data_time, 10, 164, 10, Id='When', font_path=font)
    screen.WriteAll()

    print "Updated at " + now + " with data timed " + data_time

    time.sleep(600)
