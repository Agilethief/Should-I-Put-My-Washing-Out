import urllib.request

# Docs https://open-meteo.com/en/docs
# https://api.open-meteo.com/v1/forecast?latitude=-35.28&longitude=149.13&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,rain,cloudcover,windspeed_80m,is_day
# https://api.open-meteo.com/v1/forecast?latitude=-35.28&longitude=149.13&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,rain,cloudcover,windspeed_80m,is_day&models=best_match&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&current_weather=true&forecast_days=1
# https://api.open-meteo.com/v1/forecast?latitude=-35.28&longitude=149.13&current_weather=true


def GetWeatherData(long_lat):
    url = "https://api.open-meteo.com/v1/forecast?latitude=" + \
        str(long_lat[1]) + "&longitude=" + \
        str(long_lat[0]) + \
        "&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,precipitation_probability,precipitation,cloudcover,visibility,evapotranspiration,windspeed_10m&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,uv_index_max,rain_sum,precipitation_hours,windspeed_10m_max,windgusts_10m_max&current_weather=true&forecast_days=1&timezone=Australia%2FSydney"

    # url = "https://api.open-meteo.com/v1/forecast?latitude=-35.28&longitude=149.13&hourly=temperature_2m"
    contents = urllib.request.urlopen(url).read()
    return contents
