from flask import Flask, render_template, redirect, url_for, request
# from WeatherApp/weatherdata/main import CreateReport
from weatherdata import main as weatherProgram
import json

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        print("POST")
        return redirect(url_for("templatetest"))
    else:
        print("GET")
        return render_template("ShouldI.html")


@app.route("/TemplateTest/")
def templatetest():
    return render_template("ShouldI.html")


@app.route('/CheckWeather', methods=['POST'])
def CheckWeather():
    print("== Post recieved, Server checking weather ==")
    requestData = request.get_json()
    print(requestData)
    # Validate and add user to data base here
    postcode = requestData['postcode']

    weatherData = weatherProgram.call_ShouldIPutMyWashingOut(postcode)
    print(weatherData)
    if weatherData["result"] == False:
        return {
            "reason": weatherData['reason'],
            "pass": "failed",
        }

    return {
        "pass": "success",
        "currenttime": str(weatherData['currenttime']),
        "currenthour": str(weatherData['currenthour']),
        "weather_scan_time": str(weatherData['weather_scan_time']),
        "temp": weatherData['temp'],
        "temp_2h": weatherData['temp_2h'],
        "tempMax":  weatherData['tempMax'],
        "tempMin":  weatherData['tempMin'],
        "tempCooling":  weatherData['tempCooling'],
        "windspeed":  weatherData['windspeed'],
        "windspeed_2h":  weatherData['windspeed_2h'],
        "timeToChange": str(weatherData['timeToChange']),
        "timeOfSunset": str(weatherData['timeOfSunset']),
        "timeOfSunrise":  str(weatherData['timeOfSunrise']),
        "isDaytime":  weatherData['isDaytime'],
        "precipitationProbability": weatherData['precipitationProbability'],
        "precipitationProbability_2h":  weatherData['precipitationProbability_2h'],
        "precipitation":  weatherData['precipitation'],
        "precipitation_2h": weatherData['precipitation_2h'],
        "precipitationIncreasing":  weatherData['precipitationIncreasing'],
        "cloudCover": weatherData['cloudCover'],
        "cloudCover_2h":  weatherData['cloudCover_2h'],
        "cloudCoverIncreasing": weatherData['cloudCoverIncreasing'],
        "humidity": weatherData['humidity'],
        "humidity_2h":  weatherData['humidity_2h'],
        "humidityIncreasing": weatherData['humidityIncreasing'],
        "dewpoint": weatherData['dewpoint'],
        "evapotranspiration": weatherData['evapotranspiration'],
        "WillItDry":  weatherData['WillItDry'],
        "TimeToDry": weatherData['TimeToDry'],
        "reason": weatherData['reason']
    }
