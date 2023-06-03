// page vars
var loadSpinner = document.getElementById("loadSpinner");
var result = document.getElementById("result");

loadSpinner.style.display = "none";
result.style.display = "none";

var weatherInfo = {
  temperature: {
    name: "Temperature",
    icon: "/static/images/WeatherIcons/OutlineIcon/temperature.png",
    unit: "c",
    lookup: "temp",
    include2H: true,
    longLookup: "temp_2h",
  },
  rain: {
    name: "Rain",
    icon: "/static/images/WeatherIcons/OutlineIcon/rain.png",
    unit: "mm",
    lookup: "precipitation",
    include2H: true,
    longLookup: "precipitation_2h",
  },
  humidity: {
    name: "Humidity",
    icon: "/static/images/WeatherIcons/OutlineIcon/drop.png",
    unit: "%",
    lookup: "humidity",
    include2H: true,
    longLookup: "humidity_2h",
  },
  wind: {
    name: "Wind",
    icon: "/static/images/WeatherIcons/OutlineIcon/wind.png",
    unit: "kph",
    lookup: "windspeed",
    include2H: true,
    longLookup: "windspeed_2h",
  },
  cloud: {
    name: "Cloud Cover",
    icon: "/static/images/WeatherIcons/OutlineIcon/cloud.png",
    unit: "%",
    lookup: "cloudCover",
    include2H: true,
    longLookup: "cloudCover_2h",
  },
  sunset: {
    name: "Time of Sunset",
    icon: "/static/images/WeatherIcons/OutlineIcon/sunset-.png",
    unit: "",
    lookup: "timeOfSunset",
    include2H: false,
  },
};

/*
duration = 1;
for (var key in weatherInfo) {
  var value = weatherInfo[key];

  var targetEl = "testBox";

  if (value["include2H"] == false) {
    InsertHTML(
      targetEl,
      BuildInfoCard(value["name"], value["icon"], 100, value["unit"])
    );
  } else {
    InsertHTML(
      targetEl,
      BuildLongInfoCard(value["name"], value["icon"], 20, 3, value["unit"])
    );
  }
  fadeIn(value["name"], duration);
  duration += 0.1;
}
*/

// For blocking form page reloads
var form = document.getElementById("formId");
var formIDtoCheck = 0;
function formBlocker(event) {
  event.preventDefault(); // Stops page reload
  const formData = new FormData(form); // Get the data
  formIDtoCheck = formData.get("idToCheck"); // Pull the specific data
  return false;
}
form.addEventListener("submit", formBlocker);

function ShouldIPutMyWashingOut() {
  const formData = new FormData(form); // Get the data
  postcode = formData.get("postcode"); // Pull the specific data
  console.log("ShouldIPutMyWashingOut() called for " + postcode);
  CheckWeather(postcode);
}

async function CheckWeather(postcode) {
  //console.log("Get Wisdom example fetch: " + idToCheck);

  const jsonData = JSON.stringify({ postcode: postcode });
  //console.log(jsonData);

  const getAPI = "/CheckWeather";
  //console.log(getAPI);
  const requestOptions = {
    method: "POST",
    headers: { Accept: "application/json", "Content-Type": "application/json" },
    body: jsonData,
  };

  loadSpinner.style.display = "block";
  //foundCourseElement.style.display = "none";

  let response = await fetch(getAPI, requestOptions);

  let responseData = await response.json();
  //console.log(responseData);
  if (responseData["pass"] == "success") {
    WeatherReturned(responseData);
    loadSpinner.style.display = "none";
    searchBox = document.getElementById("searchBox");
    searchBox.style.display = "none";
    console.log("Weather returned:" + responseData.temp);
    return responseData;
  } else {
    loadSpinner.style.display = "none";
    alert("Error: " + responseData["pass"]);
    console.log("Failed to load weather data");
    return null;
  }
}

function WeatherReturned(weatherData) {
  result.style.display = "block";
  console.log(weatherData);

  var resultCardContent = document.getElementById("resultCardContent");
  bounceIn("result", 1.1);
  var resultTime = document.getElementById("resultTime");

  console.log(weatherData.WillItDry);
  if (weatherData.WillItDry == true) {
    console.log("It will dry!");
    resultCardContent.innerHTML = "Yes!";

    resultTime.innerHTML = "It will dry by " + weatherData.DryTime;
  } else {
    resultCardContent.innerHTML = "No!";
    resultTime.innerHTML = weatherData.reason;
  }

  duration = 1;
  for (var key in weatherInfo) {
    var value = weatherInfo[key];

    if (value["include2H"] == false) {
      InsertHTML(
        "InfoBox",
        BuildInfoCard(
          value["name"],
          value["icon"],
          weatherData[value["lookup"]],
          value["unit"]
        )
      );
    } else {
      InsertHTML(
        "InfoBox",
        BuildLongInfoCard(
          value["name"],
          value["icon"],
          weatherData[value["lookup"]],
          weatherData[value["longLookup"]],
          value["unit"]
        )
      );
    }
    fadeIn(value["name"], duration);
    duration += 0.1;
  }
}

// // // // EFFECTS // // // //
function fadeIn(targetElementId, duration = 1) {
  var targetEl = document.getElementById(targetElementId);
  targetEl.classList.add("animate__animated", "animate__fadeInUp");
  targetEl.style.setProperty("--animate-duration", `${duration}s`);
}

function bounceIn(targetElementId, duration = 1) {
  var targetEl = document.getElementById(targetElementId);
  targetEl.classList.add("animate__animated", "animate__bounceIn");
  targetEl.style.setProperty("--animate-duration", `${duration}s`);
}

// This function will build the HTML required for inserting into a HTML element
function BuildInfoCard(cardName, cardIcon, cardValue, cardUnit) {
  var builtHTML = `  <div class="column is-one-third has-text-centered" id="${cardName}">
    <div class="box block px-1">
      <p class="heading">${cardName}</p>
      <div class="level">
        <div class="level-item">
          <img src="${cardIcon}" alt="" class="image is-64x64" />
        </div>
        <div class="level-item">
          <p id="${cardName}Content" class="title">${cardValue}<sup>${cardUnit}</sup></p>
        </div>
      </div>
    </div>
  </div>
  `;
  return builtHTML;
}

function BuildLongInfoCard(
  cardName,
  cardIcon,
  cardValue,
  cardValueLong,
  cardUnit
) {
  var builtHTML = `  <div class="column is-one-third has-text-centered" id="${cardName}">
    <div class="box block px-1">
      <p class="heading">${cardName}</p>
      <div class="level">
        <div class="level-item">
          <img src="${cardIcon}" alt="" class="image is-64x64" />
        </div>
        <div class="level-item">
          <p id="${cardName}Content" class="title">${cardValue}<sup>${cardUnit}</sup></p>
        </div>
      </div>
      <p class="heading">${cardName} in 2 hours</p>
      <div class="level">
        <div class="level-item">
          <img src="${cardIcon}" alt="" class="image is-64x64" />
        </div>
        <div class="level-item">
          <p id="${cardName}Content" class="title">${cardValueLong}<sup>${cardUnit}</sup></p>
        </div>
      </div>
    </div>
  </div>
  `;
  return builtHTML;
}

// This function is used to insert HTML into an element
function InsertHTML(elementId, html) {
  var element = document.getElementById(elementId);
  element.innerHTML += html;
}
