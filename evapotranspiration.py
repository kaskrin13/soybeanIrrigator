import math
import datetime
from multiprocessing import Pool
import processing

dailyHtmlUrls = [#("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2019-0001", 33.724016, -88.660337, "Aberdeen VTcr"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2010", 33.0443, -90.36007, "Bee Lake"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2006", 33.2599, -88.56284, "Brooksville"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2019-0002", 33.255518, -88.523615, "Brooksville 2 VTso"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2019-0003", 32.211632, -90.52006, "Brown Loam Exp Stn VT"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2019", 32.21022, -90.51228, "Brown Loam Exp Stn"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/DS-0003", 32.666566, -90.968841, "Catladge Farm"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2018-0006", 34.055236, -90.607399, "Clarksdale VTso"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DS-0002", 33.758496, -90.815173, "Cleveland"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2020", 30.44102, -88.943683, "Coastal Res & Ext Cnt"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/COOP-Stoneville", 33.431177, -90.910764, "COOP Stoneville"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DS-0001", 34.07339, -90.482674, "Cypress Farm"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2018-0007", 33.141325, -91.016638, "Longwood VTso"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2001", 34.24959, -90.54206, "Lyon"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2019-0008", 33.1469, -88.51698, "Macon VTcr"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2019-0011", 33.697351, -90.223140, "Money VT"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2013", 33.87123, -90.70963, "Mound Bayou"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2021", 33.47299, -88.77677, "MSU North Farm Starkville"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2018-0005", 34.86729, -89.996174, "Olive Branch VTcr"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2018-0009", 34.844124, -89.877597, "Olive Branch 2 VTcr"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2018-0010", 32.76372, -91.075301, "Onward VT"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/COOP-0002", 34.138698, -89.006969, "Pontotoc AWS COOP"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2007", 33.79764, -88.65915, "Prairie"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2003", 33.4187, -90.232725, "Sidon"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2004", 33.43122, -90.91077, "Stoneville AWS"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2015", 33.416512, -90.913961, "Stoneville F10"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2014", 33.42269, -90.957882, "Stoneville W"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2009", 33.40542, -90.92729, "Stoneville SW"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2002", 33.358198, -90.502738, "Thighman"),
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2018-0012", 33.95679, -90.1657, "Tippo VT"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2008", 33.35236, -90.80201, "Tribbett"),
                ("http://deltaweather.extension.msstate.edu/30-days-daily-table/DREC-2005", 34.16466, -88.72394, "Verona")]#,
                #("http://deltaweather.extension.msstate.edu/30-days-daily-table/VT2018-0004", 34.166325, -88.734339, "Verona VTso")]

hourlyHtmlUrls = [#("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2019-0001", "Aberdeen VTcr"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2010", "Bee Lake"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2006", "Brooksville"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2019-0002", "Brooksville 2 VTso"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2019-0003", "Brown Loam Exp Stn VT"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2019", "Brown Loam Exp Stn"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DS-0003", "Catladge Farm"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2018-0006", "Clarksdale VTso"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DS-0002", "Cleveland"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2020", "Coastal Res & Ext Cnt"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/COOP-Stoneville", "COOP Stoneville"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DS-0001", "Cypress Farm"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2018-0007", "Longwood VTso"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2001", "Lyon"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2019-0008", "Macon VTcr"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2019-0011", "Money VT"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2013", "Mound Bayou"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2021", "MSU North Farm Starkville"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2018-0005", "Olive Branch VTcr"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2018-0009", "Olive Branch 2 VTcr"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2018-0010", "Onward VT"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/COOP-0002", "Pontotoc AWS COOP"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2007", "Prairie"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2003", "Sidon"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2004", "Stoneville AWS"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2015", "Stoneville F10"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2014", "Stoneville W"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2009", "Stoneville SW"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2002", "Thighman"),
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2018-0012", "Tippo VT"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2008", "Tribbett"),
            ("http://deltaweather.extension.msstate.edu/7-days-hourly-table/DREC-2005", "Verona")]#,
            #("http://deltaweather.extension.msstate.edu/7-days-hourly-table/VT2018-0004", "Verona VTso")]



def DegreesToRad(latitude):
    return latitude * (math.pi/180)

def WindDirection(degDirection, windspeed):
    if (0 <= degDirection <= 11.25 or 348.75 <= degDirection <= 360):
        windspeed = str(windspeed) + " N"
    elif (11.25 < degDirection <= 33.75):
        windspeed = str(windspeed) + " NNE"
    elif (33.75 < degDirection <= 56.25):
        windspeed = str(windspeed) + " NE"
    elif (56.25 < degDirection <= 78.75):
        windspeed = str(windspeed) + " ENE"
    elif (78.75 < degDirection <= 101.25):
        windspeed = str(windspeed) + " E"
    elif (101.25 < degDirection <= 123.75):
        windspeed = str(windspeed) + " ESE"
    elif (123.75 < degDirection <= 146.25):
        windspeed = str(windspeed) + " SE"
    elif (146.25 < degDirection <= 168.75):
        windspeed = str(windspeed) + " SSE"
    elif (168.75 < degDirection <= 191.25):
        windspeed = str(windspeed) + " S"
    elif (191.25 < degDirection <= 213.75):
        windspeed = str(windspeed) + " SSW"
    elif (213.75 < degDirection <= 236.25):
        windspeed = str(windspeed) + " SW"
    elif (236.25 < degDirection <= 258.75):
        windspeed = str(windspeed) + " WSW"
    elif (258.75 < degDirection <= 281.25):
        windspeed = str(windspeed) + " W"
    elif (281.25 < degDirection <= 303.75):
        windspeed = str(windspeed) + " WNW"
    elif (303.75 < degDirection <= 326.25):
        windspeed = str(windspeed) + " NW"
    elif (326.25 < degDirection <= 348.75):
        windspeed = str(windspeed) + " NNW"
    return windspeed

# Estimates extraterrestial radiation
def EtRadiation(latitude, nDate):                                                           #φ, J
    latRad = DegreesToRad(latitude)                                                     #φ
    solarConstant = 0.0820                                                                  #Gsc
    nDay = nDate                                                                            #J
    inverseRelativeDistance = 1 + 0.033 * math.cos(((2 * math.pi)/365) * nDay)               #dr
    solarDeclination = 0.409 * math.sin(((2 * math.pi)/365) * nDay - 1.39)                  #δ
    sunsetHourAngle = math.acos(-math.tan(latRad) * math.tan(solarDeclination))  #ωs
    etRad = ((24*60)/math.pi) * solarConstant * inverseRelativeDistance * (sunsetHourAngle * math.sin(latRad) * 
    math.sin(solarDeclination) + math.cos(latRad) * math.cos(solarDeclination) * math.sin(sunsetHourAngle))
    return etRad


# Estimates evapotranspiration with the Hargreaves Method
# from Evaluation of alternative methods for estimating reference evapotranspiration by Daniel K. Fisher, H. C. Pringle III
def EvapoTranspiration(tMax, tMin, etRad):
    tMaxC = (tMax - 32) * (5/9)
    tMinC = (tMin - 32) * (5/9)
    tMeanC = (tMaxC + tMinC) / 2
    solarRad = 0.16  * (tMaxC - tMinC)**0.5 * etRad
    evapoT = 0.0133 * (tMeanC / (tMeanC + 15)) * ((23.886 * solarRad + 50)/25.4)
    return evapoT


def scheduling(evapoT):
    return 1    


def DailyChart(HTMLtup):
    data = processing.GetDailyDataFromHTML(HTMLtup[0])
    
    et = []
    for i in range(1, len(data)):
        tMax = data[i][2]
        tMin = data[i][4]
        etRad = EtRadiation(HTMLtup[1], data[i][1])
        evapoT = EvapoTranspiration(tMax, tMin, etRad)
        et.append(round(evapoT, 2))

    temperatures = []
    rainfall = []
    humidity = []
    date = []

    for i in range(1, len(data)):
        temperatures.append((data[i][2]+data[i][4])/2)
        rainfall.append(data[i][12])
        humidity.append((data[i][7]+data[i][9])/2)
        date.append(data[i][0])
    
    chart = [HTMLtup[3], date, temperatures, et, rainfall, humidity]
    return chart



def HourlyData(HTMLtup):
    data = processing.GetHourlyDataFromHTML(HTMLtup[0])
    if (not data):
        return [HTMLtup[1]]
    tMax = processing.GetHighTemp(data)[0]
    tMin = processing.GetLowTemp(data)[0]
    time = datetime.datetime.strptime(data[-1][0] + " " + data[-1][1], '%m/%d/%Y %H:%M:%S')
    temp = data[-1][7]
    humidity = data[-1][12]
    windspeed = WindDirection(data[-1][15], data[-1][14])
    rainfall = data[-1][13]
    moreThanAnHour = processing.UpdatedLastHour(processing.MakeTimeAware(time))
    tableData = [HTMLtup[1], time.time().strftime('%H:%M'), temp, windspeed, humidity, tMin, tMax, rainfall, moreThanAnHour]

    return tableData
        


def Threader(func, lst):
    p = Pool(len(lst))
    results = p.map(func, lst)
    return results