// Setup collapsibles
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function () {
    console.log("Collapsible clicked");
    this.style.display = "none";
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(
    document.querySelectorAll(".navbar-burger"),
    0
  );

  // Add a click event on each of them
  $navbarBurgers.forEach((el) => {
    el.addEventListener("click", () => {
      // Get the target from the "data-target" attribute
      const target = el.dataset.target;
      const $target = document.getElementById(target);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      el.classList.toggle("is-active");
      $target.classList.toggle("is-active");
    });
  });
});

DetermineNightDay();
createTrees(4);
createRocksLarge(1);
createRocksSmall(5);
//createMountains(1);
createLeftClouds(1);
createRightClouds(1);

function SetSunMoon(nighttime) {
  var sunContainer = document.getElementById("bgSun");
  if (nighttime) {
    // Nighttime
    sunContainer.innerHTML = `<img class="bgImage bgSun" src="/static/images/WeatherIcons/BlackIcon/015-night.png"></img>`;
    // Create new item and give it the .bgNight class
    nightTint = document.createElement("div");
    nightTint.classList.add("bgNightTint");
    sunContainer.appendChild(nightTint);
  } else {
    // Daytime
    sunContainer.innerHTML = `<img class="bgImage bgSun" src="/static/images/WeatherIcons/BlackIcon/003-sun.png"></img>`;
  }
}

function DetermineNightDay() {
  var currentHour = new Date().getHours();

  if (currentHour < 6 || currentHour >= 18) {
    SetSunMoon(true);
  } else {
    SetSunMoon(false);
  }
}

function createImage(
  src,
  xposMin,
  xPosMax,
  yPosMin,
  yPosMax,
  sizeMin,
  sizeMax
) {
  // Spawn the image
  xpos = Math.random() * (xPosMax - xposMin) + xposMin;
  ypos = Math.random() * (yPosMax - yPosMin) + yPosMin;
  newImage = createParticle(xpos, ypos, sizeMin, sizeMax);
  newImage.innerHTML = `<img class="bgImage bgTreeBase" src="${src}">`;
}

function createLeftClouds(cloudCount) {
  srcs = [
    "/static/images/WeatherIcons/BlackIcon/009-clouds.png",
    "/static/images/WeatherIcons/BlackIcon/010-clouds-1.png",
  ];
  for (let i = 0; i < cloudCount; i++) {
    src = srcs[Math.floor(Math.random() * srcs.length)];
    createImage(src, 0, 25, 40, 80, 40, 80);
  }
}
function createRightClouds(cloudCount) {
  srcs = [
    "/static/images/WeatherIcons/BlackIcon/009-clouds.png",
    "/static/images/WeatherIcons/BlackIcon/010-clouds-1.png",
  ];
  for (let i = 0; i < cloudCount; i++) {
    src = srcs[Math.floor(Math.random() * srcs.length)];
    createImage(src, 70, 100, 40, 80, 40, 80);
  }
}

function createMountains(rockCount) {
  src = "/static/images/WeatherIcons/BlackIcon/020-cave.png";
  for (let i = 0; i < rockCount; i++) {
    createImage(src, 0, 100, 19.5, 19.5, 30, 100);
  }
}

function createRocksLarge(rockCount) {
  src = "/static/images/WeatherIcons/BlackIcon/019-stone.png";
  for (let i = 0; i < rockCount; i++) {
    createImage(src, 0, 100, 5, 12, 40, 60);
  }
}

function createRocksSmall(rockCount) {
  src = "/static/images/WeatherIcons/BlackIcon/019-stone_01.png";
  for (let i = 0; i < rockCount; i++) {
    createImage(src, 0, 100, 5, 12, 40, 60);
  }
}

function createTrees(treeCount) {
  srcs = [
    "/static/images/WeatherIcons/BlackIcon/021-tree.png",
    "/static/images/WeatherIcons/BlackIcon/022-tree-1.png",
    "/static/images/WeatherIcons/BlackIcon/023-tree-2.png",
  ];

  for (let i = 0; i < treeCount; i++) {
    src = srcs[Math.floor(Math.random() * srcs.length)];
    createImage(src, 0, 100, 20, 20, 20, 100);
  }
}

function createParticle(x, y, sizeMin, sizeMax) {
  const particle = document.createElement("particle");
  particle.classList.add("bgParticle");
  let parent = document.getElementById("bgItems");
  parent.appendChild(particle);

  // Set size
  let size = Math.floor(Math.random() * sizeMax + sizeMin);

  particle.style.width = `${size}px`;
  particle.style.height = `${size}px`;

  // Set position from top left of screen
  particle.style.left = `${x}%`;
  particle.style.bottom = `${y}%`;

  return particle;
}
