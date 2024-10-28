import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import *
import math

def plusOrminusOrzero(temperatureV):
    if '-' in temperatureV:
        return temperatureV
    elif '0' == temperatureV:
        return temperatureV
    else:
        return "+" + temperatureV

CellLenght = 18

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
}



def Temperature(time, ToDayHtml):
    now = int(time)
    i = 0
    for foo in ToDayHtml.find_all('temperature-value'):

        if i * 3 == now or i * 3 - 1 == now or i * 3 + 1 == now:
            temperature = foo
            return plusOrminusOrzero(temperature['value'])

        i += 1

def Weather(ToDayWe):
    weather = []

    i = 0
    for foo in ToDayWe.find('div', class_= 'widget-row-icon'):
        if i<8:
            weather.append(foo['data-tooltip'])
        i += 1
    return weather

def Wind(time, ToDayWin):
    now = int(time)
    i = 0
    for foo in ToDayWin.find_all('div', class_= 'row-item'):

        if i * 3 == now or i * 3 - 1 == now or i * 3 + 1 == now:
            wind = foo
            return wind['data-tooltip']

        i += 1

def line_break(line):
    line1 = "|"
    line2 = " |"
    line3 = " |"
    for j in line:
        if len(j) > CellLenght - 2 and len(j) < ((CellLenght - 2) * 2):
            lenght = j.index(',') + 1
            line1 += " " * math.ceil((CellLenght - lenght) / 2)
            for i in range(j.index(',') + 1):
                line1 += j[i]
            line1 += " " * ((CellLenght - lenght) - math.ceil((CellLenght - lenght) / 2)) + "|"
            line2 += " " * math.ceil((CellLenght - (len(j) - lenght + 1)) / 2)
            for i in range(j.index(',') + 1, len(j)):
                line2 += j[i] 
            line2 += " " * ((CellLenght - (len(j) - lenght)) - math.ceil((CellLenght - (len(j) - lenght + 1)) / 2)) + "|"
            line3 += " " * CellLenght + "|"


        elif len(j) > CellLenght - 2 and len(j) >= ((CellLenght - 2) * 2):
            lenght = j.index(',') + 1
            #настраиваем 1 строчку
            line1 += " " * math.ceil((CellLenght - lenght) / 2)
            for i in range(j.index(',') + 1):
                line1 += j[i]
            line1 += " " * ((CellLenght - lenght) - math.ceil((CellLenght - lenght) / 2)) + "|"

            #настраиваем 2 строчку
            lenght = (j[j.index(',') + 2:]).index(" ") 
            line2 += " " * math.ceil((CellLenght - lenght-1) / 2)
            for i in range((j.index(',') + 1), (j.index(',') + 1) + lenght + 1):
                line2 += j[i] 
            line2 += " " * (((CellLenght - lenght-1)) - (math.ceil((CellLenght - lenght-1) / 2))) + "|"

            #настраиваем 3 строчку
            lenght = len((j[j.index(",") +2:])[j[j.index(",") +2:].index(" ") + 2:])
            line3 += " " * (math.ceil((CellLenght - lenght) / 2))
            for i in ((j[j.index(",") +2:])[j[j.index(",") +2:].index(" ") + 2:]):
                line3 += i
            line3 += " " * (((CellLenght - lenght)) - (math.ceil((CellLenght - lenght) / 2))) + "|"

        else:
            line1 += " " * CellLenght + "|"
            line2 += " " * math.ceil((CellLenght - len(j)) / 2) + j + " " * ((CellLenght - len(j)) - math.ceil((CellLenght - len(j)) / 2)) + "|"
            line3 += " " * CellLenght + "|"
    line1 += "\n"
    line2 += "\n"
    return line1 + line2 + line3


def Weather_list(day):
    match day:
        case 1:
            ToDayURL = "https://www.gismeteo.ru/weather-orel-4432/14-day/"
            DayR = requests.get(ToDayURL, timeout=30, headers=headers)
            ToDayWe = bs(DayR.text, "html.parser") 
            ToDayHtml = bs(DayR.text, "html.parser").find('div', class_= 'widget-body').find('div', class_= 'chart').find('div', class_= 'values')
            ToDayWin = bs(DayR.text, "html.parser").find('div', class_= 'widget-body').find('div', class_= 'row-wind-gust')
        
        case 2:
            ToDayURL = "https://www.gismeteo.ru/weather-orel-4432/tomorrow/"
            DayR = requests.get(ToDayURL, timeout=30, headers=headers)
            ToDayWe = bs(DayR.text, "html.parser") 
            ToDayHtml = bs(DayR.text, "html.parser").find('div', class_= 'widget-body').find('div', class_= 'chart').find('div', class_= 'values')
            ToDayWin = bs(DayR.text, "html.parser").find('div', class_= 'widget-body').find('div', class_= 'row-wind-gust')

        case 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10:
            ToDayURL = f"https://www.gismeteo.ru/weather-orel-4432/{day}-day/"
            DayR = requests.get(ToDayURL, timeout=30, headers=headers)
            ToDayWe = bs(DayR.text, "html.parser") 
            ToDayHtml = bs(DayR.text, "html.parser").find('div', class_= 'widget-body').find('div', class_= 'chart').find('div', class_= 'values')
            ToDayWin = bs(DayR.text, "html.parser").find('div', class_= 'widget-body').find('div', class_= 'row-wind-gust')

    DayRow = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    defis = "-" * (CellLenght * 8 + 9)  
    WEtemperature = ""
    WEtime = ""
    WeWind = ""
    for i in range(8):
        DayRow[i][0] = " " * round((CellLenght - len(Temperature(i * 3, ToDayHtml))) / 2) + Temperature(i * 3, ToDayHtml) + " " * ((CellLenght - len(Temperature(i * 3, ToDayHtml))) - (round((CellLenght - len(Temperature(i * 3, ToDayHtml))) / 2)) )
        DayRow[i][1] = " " * round((CellLenght - len(Wind(i * 3, ToDayWin))) / 2) + Wind(i * 3, ToDayWin) + " " * ((CellLenght - len(Wind(i * 3, ToDayWin))) - (round((CellLenght - len(Wind(i * 3, ToDayWin))) / 2)) )
        DayRow[i][2] = " " * round((CellLenght - len(str(i * 3) + ":00")) / 2) + str(i * 3) + ":00" + " " * ((CellLenght - len(str(i * 3) + ":00")) - (round((CellLenght - len(str(i * 3) + ":00")) / 2)) )
        WEtemperature += f"|{DayRow[i][0]}"
        WEtime += f"|{DayRow[i][2]}"
        WeWind += f"|{DayRow[i][1]}"

    return (f"\n {defis} \n {WEtime}| \n {defis} \n {line_break(Weather(ToDayWe))} \n {defis} \n {WEtemperature}| \n {defis} \n {WeWind}| \n {defis} ")

def NumToWeekday(day):
    match day:
        case 0:
            return("Пн")
        case 1:
            return("Вт")
        case 2:
            return("Ср")
        case 3:
            return("Чт")
        case 4:
            return("Пт")
        case 5:
            return("Сб")
        case 6:
            return("Вс")
        
def NumToMonth(month):
    match month:
        case 1:
            return "Янв"
        case 2:
            return "Фев"
        case 3:
            return "Март"
        case 4:
            return "Апр"
        case 5:
            return "Май"
        case 6:
            return "Июнь"
        case 7:
            return "Июль"
        case 8:
            return "Авг"
        case 9:
            return "Сен"
        case 10:
            return "Окт"
        case 11:
            return "Нояб"
        case 12:
            return "Дек"

def calendar():
    defis = "-" * (10 * 10 + 2 + 9)  
    CLweek = ""
    CLday = ""
    days = []
    months = []
    for i in range(0, 10):
        ThisMonth = (datetime.now() + timedelta(days = i)).month
        Thisday = str((datetime.now() + timedelta(days = i)).day)
        days.append(Thisday)
        months.append(NumToMonth(ThisMonth))
        ThisWeekday = NumToWeekday((datetime.now() + timedelta(days = i)).weekday())
        CLweek += " " * 4 + ThisWeekday + " " * 4 + "|"
        CLday += " " * math.ceil((10 - len(Thisday + " " + NumToMonth(ThisMonth))) / 2) + Thisday + " " + NumToMonth(ThisMonth) + " " * ((10 - len(Thisday + " " + NumToMonth(ThisMonth))) - (math.ceil((10 - len(Thisday + " " + NumToMonth(ThisMonth))) / 2))) + "|"
    rez = (f"{defis} \n|{CLweek} \n{defis} \n|{CLday} \n{defis} \n")
    return rez, days, months



def main():
    UserInput = input("Введите команду для поиска по Gismeteo(c - для просмотра всех команд): ")
    match UserInput:
        case "c":
            print("td - просмотр погоды на сегодня\ntw - просмотр погоды на завтра\nte - просмотр погоды на конкретное число")
        case "td":

            print("погода и температура в орле на сегодня:", Weather_list(1))
        case "tw":

            print("погода и температура в орле на завтра:", Weather_list(2))
        case "te":
            print("Введите число, на который вы бы хотели узнать погоду: \n")
            print(calendar()[0])
            ChoosedDay = str(input()) 
            print(f"погода и температура в орле на {ChoosedDay} {calendar()[2][int(calendar()[1].index(ChoosedDay))]}:", Weather_list(int(calendar()[1].index(ChoosedDay) + 1)))
        case _:
            print("неверно введена команда")

    print("\n")
    main()

main()