
import time, datetime
import calendar
from tkinter import *
from tkinter import ttk



class OpenWeatherMap:
    def __init__(self):
        print('OpenWeatherMap object is created.')

        API_KEY = '293951899fa98a759925ed3b0451b4cd'
        API_URL = 'http://api.openweathermap.org/data/2.5/forecast?q={0}&units=metric&lang=ja&APPID={1}'

    def GetWeatherinfo(self, city_name):
        print('GetWeatherinfo : {}'.format(city_name))



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
        self.root.title('Weathermap_Raspberrypi')

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid()

        self.owm_obj = OpenWeatherMap()
        self.datetime_obj = Datetime()

        self.city_name = 'Nagoya'

        self.CreateWidget()

    
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


    def UpdateWeather(self):
        print('a')


    def UpdateCityname(self):

        self.label_cityname.configure(text = self.city_name)
        self.label_cityname.update()


    def ClickButton(self):

        for i in self.lb.curselection():
            self.city_name = self.lb.get(i)
        
        print(self.city_name)
        self.owm_obj.GetWeatherinfo(self.city_name)

        self.UpdateCityname()

    
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
        self.label_date.grid(row = 0, column = 1, columnspan = 4, padx = 30)

        #Weekday
        self.weekday_str = self.datetime_obj.GetWeekday()

        self.label_weekday = ttk.Label(self.main_frame, text = self.weekday_str, font = ("", 35))
        self.label_weekday.grid(row = 0, column = 2, columnspan = 2, pady = 30, sticky = S)

        #Irast
        #irast_info = PhotoImage(file = 'weathermap_irast.png')

        #label_irast = ttk.Label(self.main_frame, image = irast_info)
        #label_irast.grid(row = 0, column = 4, columnspan = 2, rowspan = 2)

        #Cityname
        self.label_cityname = ttk.Label(self.main_frame, text = self.city_name, font = ("", 20))
        self.label_cityname.grid(row = 1, column = 2, columnspan = 2, padx = 5, pady = 5)

        #Update
        self.UpdateDateTime()
        self.UpdateWeekday()

        self.root.mainloop()



if __name__ == '__main__':


    tkinter_obj = Tkinter()





