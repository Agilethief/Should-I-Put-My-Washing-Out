from . import postcodeConversion  # import CreateDatabase, PostCodeToLongLat
from . import weather  # import GetWeatherData
from . import report
import json
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
# from cgi import escape


def ValidatePostcodeInput(incomingpostcode):
    # Check if postcode is valid
    try:
        int(incomingpostcode)
    except:
        return False
    return True


def ValidateLongLatInput(long, lat):
    # Check if longlat is valid

    return True


def GetWeatherFromPostcode(postcode):
    print("Connecting to database...")
    postcodeConversion.CreateDatabase()
    print("Converting postcode to long and lat...")
    longlat = postcodeConversion.PostCodeToLongLat(postcode)

    print("Long Lat: ", longlat)
    if (longlat[0] == False):
        print("Postcode not found in database, returning false")
        return False

    print("Getting weather data...")
    weatherdata = weather.GetWeatherData(longlat)
    weatherdata = json.loads(weatherdata)

    with open("weatherdata/TestOutput/weatherdata.json", "w") as outfile:
        outfile.write(str(weatherdata))

    return weatherdata


def GetWeatherFromLongLat(long, lat):
    longlat = (long, lat)
    print("Getting weather data...")
    weatherdata = weather.GetWeatherData(longlat)
    weatherdata = json.loads(weatherdata)

    return weatherdata

# prep the weather data for use in a dict.


def PrepareWeatherData(weatherdata):
    # Current Time
    currentTime = datetime.now().time().strftime('%H:%M')
    currentTime = datetime.strptime(currentTime, "%H:%M")
    # Important for getting the right time from the weatherdata
    currentHour = currentTime.hour
    currentHour_2h = min(currentHour + 2, 23)

    # Unpacking JSON
    current_weather = weatherdata['current_weather']
    daily_weather = weatherdata['daily']
    daily_units = weatherdata['daily_units']
    hourly_weather = weatherdata['hourly']

    # Current weather
    weather_scan_time = current_weather['time']
    temp = current_weather['temperature']
    temp_2h = hourly_weather['temperature_2m'][currentHour_2h]
    tempMax = daily_weather['temperature_2m_max'][0]
    tempMin = daily_weather['temperature_2m_min'][0]
    tempCooling = temp_2h < temp

    # Wind
    windspeed = current_weather['windspeed']
    windspeed_2h = hourly_weather['windspeed_10m'][currentHour_2h]

    # Sunset and rise times
    timeToChange = TimeToSunchange(weatherdata)
    timeOfSunset = weatherdata['daily']['sunset'][0]
    timeOfSunrise = weatherdata['daily']['sunrise'][0]
    isDaytime = current_weather['is_day']

    # Rain
    precipitationProbability = hourly_weather['precipitation_probability'][currentHour]
    precipitationProbability_2h = hourly_weather['precipitation_probability'][currentHour_2h]
    precipitation = hourly_weather['precipitation'][currentHour]
    precipitation_2h = hourly_weather['precipitation'][currentHour_2h]
    precipitationIncreasing = precipitation_2h > precipitation

    # Cloud cover
    cloudCover = hourly_weather['cloudcover'][currentHour]
    cloudCover_2h = hourly_weather['cloudcover'][currentHour_2h]
    cloudCoverIncreasing = cloudCover_2h > cloudCover

    # Humidity
    humidity = hourly_weather['relativehumidity_2m'][currentHour]
    humidity_2h = hourly_weather['relativehumidity_2m'][currentHour_2h]
    humidityIncreasing = humidity_2h > humidity
    dewpoint = hourly_weather['dewpoint_2m'][currentHour]
    evapotranspiration = hourly_weather['evapotranspiration'][currentHour]

    # Return dictionary of weather data
    return {
        "currenttime": currentTime,
        "currenthour": currentHour,
        "weather_scan_time": weather_scan_time,
        "temp": temp,
        "temp_2h": temp_2h,
        "tempMax": tempMax,
        "tempMin": tempMin,
        "tempCooling": tempCooling,
        "windspeed": windspeed,
        "windspeed_2h": windspeed_2h,
        "timeToChange": timeToChange,
        "timeOfSunset": timeOfSunset,
        "timeOfSunrise": timeOfSunrise,
        "isDaytime": isDaytime,
        "precipitationProbability": precipitationProbability,
        "precipitationProbability_2h": precipitationProbability_2h,
        "precipitation": precipitation,
        "precipitation_2h": precipitation_2h,
        "precipitationIncreasing": precipitationIncreasing,
        "cloudCover": cloudCover,
        "cloudCover_2h": cloudCover_2h,
        "cloudCoverIncreasing": cloudCoverIncreasing,
        "humidity": humidity,
        "humidity_2h": humidity_2h,
        "humidityIncreasing": humidityIncreasing,
        "dewpoint": dewpoint,
        "evapotranspiration": evapotranspiration
    }


def PrintWeatherData(weatherdata):
    # Current Time

    print("Current time: ", weatherdata['currenttime'])
    print("Current hour:", weatherdata['currenthour'])

    # Current weather
    print("Weather scan time: ", weatherdata['weather_scan_time'])
    print("Temp: ", weatherdata['temp'])
    print("Temp cooling?: ", "TODO")
    print("Temp Day Max: ", weatherdata['tempMax'])
    print("Temp Day Min: ", weatherdata['tempMin'])

    # Wind
    print("Windspeed: ", weatherdata['windspeed'])

    # Sunset and rise times

    if (weatherdata['isDaytime'] == 1):
        print("Sun is in the sky")
        print("Sunset time: ", weatherdata['timeOfSunset'])
        print("Time to sunset", weatherdata['timeToChange'].hour,
              "hours and", weatherdata['timeToChange'].minute, "minutes")
    else:
        print("Sun has set")
        print("Sunset time: ", weatherdata['timeOfSunrise'])
        print("Time to sun rise", weatherdata['timeToChange'].hour,
              "hours and", weatherdata['timeToChange'].minute, "minutes")

    # Rain
    print("Rain probability: ",
          weatherdata['precipitationProbability'])
    print("Rain amount", weatherdata['precipitation'], "mm")

    # Cloud cover
    print("Cloud Cover", weatherdata['cloudCover'], "%")

    print("Humidity", weatherdata['humidity'], "%")


def TimeToSunchange(weatherdata):
    current_daily = weatherdata['daily']

    sunrise = (current_daily['sunrise'][0])
    sunrise = datetime.strptime(sunrise, "%Y-%m-%dT%H:%M")
    sunset = (current_daily['sunset'][0])
    sunset = datetime.strptime(sunset, "%Y-%m-%dT%H:%M")
    currentTime = datetime.now().time().strftime('%H:%M')
    currentTime = datetime.strptime(currentTime, "%H:%M")

    if (currentTime < sunset):
        print("It is before sunset")
        timeToSunChange = sunset - currentTime
    elif (currentTime < sunrise):
        print("It is before sunrise")
        timeToSunChange = sunrise - currentTime
    else:
        print("It is after sunset")
        timeToSunChange = sunrise - currentTime

    hours = timeToSunChange.seconds // 3600
    minutes = (timeToSunChange.seconds // 60) % 60

    print("=== Time to sun change ===")
    print("Current time: ", currentTime)
    print("Sunrise: ", sunrise)
    print("Sunset: ", sunset)

    print("=== Time to sun change ===")

    return time((int(hours)), (int(minutes)))


def HardWeatherChecks(weatherdata):
    # Night time prevents ability to dry.
    if (weatherdata['isDaytime'] == False):
        print("No, weather conditions are not appropriate:", "It is night time")
        return (False, "It is night time")

    if (weatherdata['timeToChange'].hour < 1):
        print("No, weather conditions are not appropriate:",
              "It will be night time soon")
        return (False, "It will be night time soon")

    # High Rain reduces ability to dry.
    # if rain is over 1mm per hour return false
    if (weatherdata['precipitation'] > 1 or weatherdata['precipitation_2h'] > 1):
        print("No, weather conditions are not appropriate:",
              "It is raining")
        return (False, "It is raining")

    return (True, "Weather is fine")


def ShouldYouPutYourWashingOut(weatherdata):
    print("Should you put your washing out? ")

    timeToDry = 24
    reason = "Undetermined"

    # Hard cut off points to check.
    hardWeatherCheck = HardWeatherChecks(weatherdata)
    if (hardWeatherCheck[0] == False):
        reason = hardWeatherCheck[1]
        return (False, timeToDry, reason)

    # Determine how many hours based on temp alone.
    avgTemp = (weatherdata['temp'] + weatherdata['temp_2h']) / 2
    timeToDry = GetDryTimeFromTemp(
        avgTemp, weatherdata['tempCooling'])

    # High Cloud cover reduces ability to dry.
    avgCloudCover = (weatherdata['cloudCover'] +
                     weatherdata['cloudCover_2h']) / 2
    timeToDry = ApplyCloudCoverageToDryTime(timeToDry, avgCloudCover)

    # High humidity increases time to dry
    avgHumidity = (weatherdata['humidity'] +
                   weatherdata['humidity_2h']) / 2
    timeToDry = ApplyHumidityToDryTime(timeToDry, avgHumidity)

    # High wind decreases time to dry
    timeToDry = ApplyWindToDryTime(timeToDry, weatherdata['windspeed'])

    timeToDry = ApplyRainToDryTime(timeToDry, weatherdata['precipitation'])

    print("Time to dry:", timeToDry, "hours")
    print("Time to change: ", weatherdata['timeToChange'].hour, "hours")
    print("Time to Sunset:", weatherdata['timeOfSunset'], "hours")
    print("Time to Sunrise:", weatherdata['timeOfSunrise'], "hours")
    if (timeToDry > weatherdata['timeToChange'].hour):
        return (False, timeToDry, "It will be night time before it dries.")

    print("Yes, conditions are appropriate")
    print("Time to dry:", timeToDry, "hours")
    if (timeToDry > 10):
        return (False, timeToDry)
    return (True, timeToDry, reason)


def GetDryTimeFromTemp(temp, cooling=False):
    coolingmodifier = 1
    drytime = 5
    if (cooling):
        coolingmodifier = 1.5

    drytime = lerp(5, 0.5, temp / 35) * coolingmodifier
    print("Dry time from temp:", drytime, "hours", "Temp:", temp, "C")
    return drytime


def ApplyCloudCoverageToDryTime(drytime, cloudCover):
    cloudEffect = lerp(1.8, 1, cloudCover / 100)
    print("Dry time from cloud cover:", drytime * cloudEffect,
          "hours", "Cloud Cover:", cloudCover, "%")
    return drytime * cloudEffect


def ApplyHumidityToDryTime(drytime, humidity):
    # Greater than 80 humidity = 3x time to dry
    # Less than 80 humidity = 1.5x time to dry
    if humidity > 80:
        humidityEffect = lerp(1, 3, humidity / 100)
        print("Dry time from humidity:", drytime *
              humidityEffect, "hours", "Humidity:", humidity, "%")
        return drytime * humidityEffect
    else:
        humidityEffect = lerp(1, 2, humidity / 100)
        print("Dry time from humidity:", drytime *
              humidityEffect, "hours", "Humidity:", humidity, "%")
        return drytime * humidityEffect


def ApplyWindToDryTime(drytime, windspeed):
    # wind maxes at 40kph,
    windEffect = lerp(1, 0.1, windspeed / 34)
    print("Dry time from wind:", drytime * windEffect,
          "hours ==", "Wind:", windspeed, "kph")
    return drytime * windEffect


def ApplyRainToDryTime(drytime, rain):
    rainEffect = lerp(1, 2, rain / 1)
    print("Dry time from rain:", drytime *
          rainEffect, "hours", "Rain:", rain, "mm")
    return drytime * rainEffect


def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b


'''
This is a primary thing that the website will call.
'''


def call_ShouldIPutMyWashingOut(postcodeInput):
    # Validate and protect from the input.
    if (ValidatePostcodeInput(postcodeInput) == False):
        print("Invalid postcode")
        return {"result": False, "reason": "Invalid postcode"}

    weatherdata = GetWeatherFromPostcode(postcodeInput)
    # Check if we can find a postcode to work with
    if (weatherdata == False):
        print("Invalid postcode")
        return {"result": False, "reason": "Postcode not found"}

    weatherdata = PrepareWeatherData(weatherdata)
    shouldWashingGoOut = ShouldYouPutYourWashingOut(weatherdata)
    weatherdata['WillItDry'] = shouldWashingGoOut[0]
    weatherdata['TimeToDry'] = shouldWashingGoOut[1]
    weatherdata['reason'] = shouldWashingGoOut[2]
    weatherdata['result'] = True

    # record this search
    report.AddWeatherSearchToDatabase(weatherdata, postcodeInput, 0, 0)

    return weatherdata


def call_ShouldIPutMyWashingOutLongLat(long, lat):
    # TODO validate input

    weatherdata = GetWeatherFromLongLat(long, lat)

    if (weatherdata == False):
        print("Invalid long lat")
        return {"result": False, "reason": "Longitude/Latitude not found"}

    weatherdata = PrepareWeatherData(weatherdata)
    shouldWashingGoOut = ShouldYouPutYourWashingOut(weatherdata)
    weatherdata['WillItDry'] = shouldWashingGoOut[0]
    weatherdata['TimeToDry'] = shouldWashingGoOut[1]
    weatherdata['reason'] = shouldWashingGoOut[2]
    weatherdata['result'] = True

    # record this search
    report.AddWeatherSearchToDatabase(weatherdata, 0, long, lat)

    return weatherdata


if __name__ == "__main__":
    postcodeInput = input("Enter postcode: ")
    weatherdata = GetWeatherFromPostcode(postcodeInput)
    weatherdata = PrepareWeatherData(weatherdata)
    shouldWashingGoOut = ShouldYouPutYourWashingOut(weatherdata)
    weatherdata['WillItDry'] = shouldWashingGoOut[0]
    weatherdata['TimeToDry'] = shouldWashingGoOut[1]
    print(weatherdata)
