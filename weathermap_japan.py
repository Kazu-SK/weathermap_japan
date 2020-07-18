
import time, datetime
import calendar
from tkinter import *
from tkinter import ttk

import json
import os
import requests
import sys

from pytz import timezone



class OpenWeatherMap:
    def __init__(self):
        print('OpenWeatherMap object is created.')

        self.API_KEY = '293951899fa98a759925ed3b0451b4cd'
        #self.API_KEY = '' #You must set your API_KEY.
        self.API_URL = 'http://api.openweathermap.org/data/2.5/forecast?q={0}&units=metric&lang=ja&APPID={1}'

        self.INFO_NUM = 5 #You must not change this number. 


    def GetWeatherinfo(self, city_name):
        print('GetWeatherinfo : {}'.format(city_name))

        weathermap_url = self.API_URL.format(city_name, self.API_KEY)

        response = requests.get(weathermap_url)
        forecastData = json.loads(response.text)


        forecast_time = []
        weather_description = []
        weather_icon = []
        city_temperature = []
        city_rainfall = []


        if not ('list' in forecastData):
            print('error')
            return

        for i, item in enumerate(forecastData['list'], 0):
            forecast_time.append(timezone('Asia/Tokyo').localize(datetime.datetime.fromtimestamp(item['dt'])))
            forecast_time[i] = forecast_time[i].strftime('%H:%M')
            weather_description.append(item['weather'][0]['description'])
            weather_icon.append(item['weather'][0]['icon'])
            city_temperature.append(item['main']['temp'])

            if 'rain' in item:
                city_rainfall.append(str(item['rain']['3h']))
            else:
                city_rainfall.append('0')

            if i == self.INFO_NUM:
                break


        print(forecastData['city']['name'])

        return forecast_time, weather_description, weather_icon, city_temperature, city_rainfall



class Datetime:
    def __init__(self):
        print('DateAndTime object is created.')

    
    def GetDatetime(self):
        datetime_now = datetime.datetime.fromtimestamp(time.time())
        datetime_str = datetime_now.strftime('%Y/%m/%d %H:%M:%S') 

        return datetime_str


    def GetWeekday(self):
        weekday_now = datetime.date.today().weekday()
        weekday_str = calendar.day_name[weekday_now]

        return weekday_str
        


class Tkinter:
    def __init__(self):
        self.root = Tk()
        self.root.title('Weathermap_Map')

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid()

        self.owm_obj = OpenWeatherMap()
        self.datetime_obj = Datetime()

        self.city_name = 'Morioka'

        self.REFERENCE_ICON = {
            "01d":"weather/01d.png","01n":"weather/01n.png",
            "02d":"weather/02d.png","02n":"weather/02n.png",
            "03d":"weather/03d03n.png","03n":"weather/03d03n.png",
            "04d":"weather/04d04n.png","04n":"weather/04d04n.png",
            "09d":"weather/09d09n.png","09n":"weather/09d09n.png",
            "10d":"weather/10d10n.png","10n":"weather/10d10n.png",
            "11d":"weather/11d11n.png","11n":"weather/11d11n.png",
            "13d":"weather/13d13n.png","13n":"weather/13d13n.png",
            "50d":"weather/50d.png"
        }

        self.forecasttime_labels = []
        self.rainfall_labels = []
        self.weather_labels = []
        self.description_labels = []
        self.temperature_labels = []

        self.icon = []

    
    def UpdateDateTime(self):

        self.dt_str = self.datetime_obj.GetDatetime()
        self.label_date.configure(text = self.dt_str)

        self.label_date.update()
        self.root.after(1000, self.UpdateDateTime)


    def UpdateWeekday(self):

        self.weekday_str = self.datetime_obj.GetWeekday()
        self.label_weekday.configure(text = self.weekday_str)

        self.label_weekday.update()
        self.root.after(1000, self.UpdateWeekday)


    def UpdateWeatherinfo(self):
        self.owm_obj.GetWeatherinfo(self.city_name)


    def UpdateCityname(self):

        self.label_cityname.configure(text = self.city_name)
        self.label_cityname.update()


    def ClickButton(self):

        for i in self.lb.curselection():
            self.city_name = self.lb.get(i)
        
        print(self.city_name)

        self.UpdateCityname()
        self.UpdateWeatherinfo()

    
    def CreateListbox(self):

        with open('japan.txt') as f:

            city_counter = 0
            
            for line in f:
                file_info = f.read()
                japan_city = file_info.splitlines()
                

        v1 = StringVar(value=japan_city)
        self.lb = Listbox(self.main_frame, listvariable = v1, height = 13)
        self.lb.grid(row=0, column=0, padx = 5, pady = 5, sticky=(N,E,S,W))

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.main_frame, 
            orient=VERTICAL, 
            command=self.lb.yview)
        self.lb['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.grid(row = 0,column = 1, rowspan = 2, sticky=(N,S,W))


    def CreateWidget(self):

        #ListBox
        self.CreateListbox()

        #Button
        self.ok_button = ttk.Button(self.main_frame, text = 'OK', command = self.ClickButton)
        self.ok_button.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = (N, E, W, S))
       
        #DateTime
        self.dt_str = self.datetime_obj.GetDatetime()

        self.label_date = ttk.Label(self.main_frame, text = self.dt_str, font = ("", 45))
        self.label_date.grid(row = 0, column = 1, columnspan = 4)

        #Weekday
        self.weekday_str = self.datetime_obj.GetWeekday()

        self.label_weekday = ttk.Label(self.main_frame, text = self.weekday_str, font = ("", 35))
        self.label_weekday.grid(row = 0, column = 2, columnspan = 2, pady = 30, sticky = S)

        #Irast
        irast_info = PhotoImage(file = 'weathermap_irast.png')

        label_irast = ttk.Label(self.main_frame, image = irast_info)
        label_irast.grid(row = 0, column = 4, columnspan = 2, rowspan = 2)

        #Cityname
        self.label_cityname = ttk.Label(self.main_frame, text = self.city_name, font = ("", 20))
        self.label_cityname.grid(row = 1, column = 2, columnspan = 2, padx = 5, pady = 5)
        
        #Weather


        weather_forecasttime, weather_description, weather_icon, city_temperature, city_rainfall = self.owm_obj.GetWeatherinfo(self.city_name)


        for i in range(6):

            self.forecasttime_labels.append(ttk.Label(self.main_frame, text = weather_forecasttime[i], font = ("", 30))) 
            self.forecasttime_labels[i].grid(row = 2, column = i, padx = 10, pady = 30)
            self.description_labels.append(ttk.Label(self.main_frame, text = weather_description[i], font = ("", 10)))
            self.description_labels[i].grid(row = 4, column = i, pady = 10)
            self.temperature_labels.append(ttk.Label(self.main_frame, text = city_temperature[i], font = ("", 30)))
            self.temperature_labels[i].grid(row = 5, column = i, padx = 30, pady = 10)
            self.rainfall_labels.append(ttk.Label(self.main_frame, text = city_rainfall[i], font = ("", 30)))
            self.rainfall_labels[i].grid(row = 6, column = i, padx = 30, pady = 10)

            self.icon.append(PhotoImage(file = self.REFERENCE_ICON[weather_icon[i]]))
            self.weather_labels.append(ttk.Label(self.main_frame, image = self.icon[i]))
            self.weather_labels[i].grid(row = 3, column = i, padx = 30, pady = 10)

        


        #Update
        self.UpdateDateTime()
        self.UpdateWeekday()
        self.UpdateWeatherinfo()

        self.root.mainloop()



if __name__ == '__main__':


    tkinter_obj = Tkinter()

    tkinter_obj.CreateWidget()





