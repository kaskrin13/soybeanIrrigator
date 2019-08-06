import datetime
import bs4
import pytz
import requests
import urllib.request
import lxml

# goes to the MSU website, finds a table on the page and inserts it into a 2d list
# then processes the data added to table (covert text to necessary formats)
# and returns the data for the past 30 days
# input: url = string
# output: data = 2d list
def GetDailyDataFromHTML(url):
    # get html from website
    html = requests.get(url, stream=True)

    # get table from html
    data = [[cell.text.strip() for cell in row('td')] for row in bs4.BeautifulSoup(html.content, "lxml")('tr')]

    # if no table is found return an empty list
    if not data:
        return data

    # add column labels
    data[0] = ['Record Date (MM / DD / YYYY)', 'Record Julian Date (NNN day of the year)', 
            'Air Temperature Max (Degrees Fahrenheit F)', 'Time Max Air Temperature (HH: MM: SS)', 
            'Air Temperature Min (Degrees Fahrenheit F)', 'Time Min Air Temperature (HH: MM: SS)', 
            'Air Temperature Observed (Degrees Fahrenheit F) instant reading at 7:00:00 ST', 
            'Relative Humidity Max (Percent)', 'Time Max Relative Humidity (HH: MM: SS)',	
            'Relative Humidity Min (Percent)', 'Time Min Relative Humidity (HH: MM: SS)', 
            'Relative Humidity Observed (Percent) instant reading at 7:00:00 ST', 'Precipitation (Inches n.nn)', 
            'Pan Evaporation (Inches n.nn)', 'Wind Run (Miles)', 'Wind Speed (Miles Per Hour)', 
            'Wind Direction (Degrees)', 'Solar Radiation (Langleys)', 
            'Soil Temperature Max at 2 inch depth (Degrees Fahrenheit F)', 'Time Max Soil temperature at 2 inches (HH: MM: SS)', 
            'Soil Temperature Min at 2 inch depth (Degrees Fahrenheit F)', 'Time Min Soil temperatures at 2 inches (HH: MM: SS)', 
            'Soil Temperature Observed at 2 inch depth (Degrees Fahrenheit F) instant reading at 7:00:00 ST', 
            'Soil Temperature Max at 4 inch depth (Degrees Fahrenheit F)', 'Time Max Soil temperatures at 4 inches (HH: MM: SS)', 
            'Soil Temperature Min at 4 inch depth (Degrees Fahrenheit F)', 'Time Min Soil temperatures at 4 inches (HH: MM: SS)', 
            'Soil Temperature Observed at 4 inch depth (Degrees Fahrenheit F) instant reading at 7:00:00 ST', 
            'DD50 Degree Days 50 Fahrenheit', 'Adjusted DD50 Degree Days 50 Fahrenheit adjusted for latitude', 
            'DD60 Degree Days 60 Fahrenheit']

    # remove last two rows, which are unnecessary
    data.pop(-1)
    data.pop(-1)

    # remove unnecessary/empty columns
    for i in range(0, len(data), 1):
        data[i] = data[i][:17]
        data[i] = data[i][:13] + data[i][15:16]

    # if data is blank use NaN (not a number)
    data = [[float('NaN') if item == '' else item for item in row] for row in data]

    # convert text to float for temperature, humidity, precipitation, and wind speed
    for i in range(1, len(data), 1):
        data[i][1] = float(data[i][1])
        data[i][2] = float(data[i][2])
        data[i][4] = float(data[i][4])
        data[i][6] = float(data[i][6])
        data[i][7] = float(data[i][7])
        data[i][9] = float(data[i][9])
        data[i][11] = float(data[i][11])
        data[i][12] = float(data[i][12])
        data[i][13] = float(data[i][13])

    return data


# goes to the MSU website, finds a table on the page and inserts it into a 2d list
# then processes the data added to table (covert text to necessary formats)
# and returns the data for the current day
def GetHourlyDataFromHTML(url):
    # get html from website
    html = requests.get(url, stream=True)

    # get table from html
    data = [[cell.text.strip() for cell in row('td')] for row in bs4.BeautifulSoup(html.content, "lxml")('tr')]

    # if no table is found return an empty list
    if not data:
        return data

    # add column labels
    data[0] = ['Record Date (MM/DD/YYYY)', 'Record Time (HH:MM:SS)', 'Record Julian Date', 
            'Air Temperature Max (Degrees Fahrenheit F)', 'Time Max Air Temperature (HH:MM:SS)',
            'Air Temperature Min (Degrees Fahrenheit F)', 'Time Min Air Temperature (HH:MM:SS)',
            'Air Temperature Observed (Degrees Fahrenheit F)', 'Relative Humidity Max (Percent)',
            'Time Max Relative Humidity (HH:MM:SS)', 'Relative Humidity Min (Percent)',
            'Time Min Relative Humidity (HH:MM:SS)', 'Relative Humidity Observed (Percent)',
            'Precipitation (Inches n.nn)', 'Wind Speed (Miles Per Hour)', 'Wind Direction (Degrees)',
            'Solar Radiation (Langleys)', 'Soil Temperature Average at 2 inch depth (Degrees Fahrenheit F)',
            'Soil Temperature Observed at 2 inch depth (Degrees Fahrenheit F)',
            'Soil Temperature Average at 4 inch depth (Degrees Fahrenheit F)',
            'Soil Temperature Observed at 4 inch depth (Degrees Fahrenheit F)']

    # remove last two rows, which are unnecessary
    data.pop(-1)
    data.pop(-1)

    # remove unnecessary columns
    for i in range(0, len(data), 1):
        data[i] = data[i][:16]

    # if data is blank use NaN (not a number)
    data = [[float('NaN') if item == '' else item for item in row] for row in data]
    # convert text to float for temperature, humidity, precipitation, and wind speed
    for i in range(1, len(data), 1):
        data[i][2] = float(data[i][2])
        data[i][3] = float(data[i][3])
        data[i][5] = float(data[i][5])
        data[i][7] = float(data[i][7])
        data[i][8] = float(data[i][8])
        data[i][10] = float(data[i][10])
        data[i][12] = float(data[i][12])
        data[i][13] = float(data[i][13])
        data[i][14] = float(data[i][14])
        data[i][15] = float(data[i][15])

    # place data from today's date in a seperate table
    todaysData = []
    today = UtcToLocal(datetime.datetime.utcnow())

    for row in data[1:]:
        if (today.date() == datetime.datetime.strptime(row[0], '%m/%d/%Y').date()):
            todaysData.append(row)

    return todaysData


# determines if daylight savings time is in effect
def DaylightSavings(zonename):
    tz = pytz.timezone(zonename)
    now = pytz.utc.localize(datetime.datetime.utcnow())
    return now.astimezone(tz).dst() != datetime.timedelta(0)



# converts datetime object from UTC to local timezone
# input: utc = datetime
# output: utc+offset = datetime
def UtcToLocal(utc):
    timezone = 'America/Chicago'
    tz = pytz.timezone('America/Chicago')
    if (DaylightSavings(timezone)):
        return pytz.utc.localize(utc).astimezone(tz)
    else:
        return pytz.utc.localize(utc, is_dst=False).astimezone(tz)



# makes a datetime object timezone aware
# input: time = datetime
# output: time = datetime
def MakeTimeAware(time):
    timezone = 'America/Chicago'
    tz = pytz.timezone('America/Chicago')
    if (not DaylightSavings(timezone)):
        return tz.localize(time, is_dst=True).astimezone(tz)
    else:
        return tz.localize(time, is_dst=False).astimezone(tz)



# checks if more than an hour has passed since the data was last updated
# returns true if it has, false if not
# input: mostRecentTime = dateTime
# output: moreThanAnHour = boolean
def UpdatedLastHour(mostRecentTime):
    # Convert now from UTC to central time
    now = UtcToLocal(datetime.datetime.utcnow())
    
    delta = now - mostRecentTime

    # Check if more than an hour and fifteen minutes has passed
    if (delta.seconds / 60) > 150:
        moreThanAnHour = True
    else:
        moreThanAnHour = False
    return moreThanAnHour



# gets lowest temperature of the day by
# searching entries in table (2d list) between the beginning
# of the current day and the last entry (most recent time)
# inputs: data = 2d list
# output: lowTemp = tuple(int, int)
def GetLowTemp(data):
    lowTemp = data[0][5]
    index = 0

    # Search new list for most lowest temp (uses most recent if there are matches)
    for i in range(0, len(data), 1):
        if (data[i][5] <= lowTemp and i > index):
            lowTemp = data[i][5]
            index = i
    return (lowTemp, index)



# gets highest temperature of the day by
# searching entries in table (2d list) between the beginning
# of the current day and the last entry (most recent time)
# inputs: data = 2d list
# output: highTemp = tuple(int, int)
def GetHighTemp(data):
    highTemp = data[0][3]
    index = 0

    # Search new list for highest temp (uses most recent if there are matches)
    for i in range(0, len(data), 1):
        if (data[i][3] >= highTemp and i > index):
            highTemp = data[i][3]
            index = i
    return (highTemp, index)



# prints the data in a readible format for error checking
# input: data = 2d list
def PrintData(data):
    s = [[str(e) for e in row] for row in data]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))