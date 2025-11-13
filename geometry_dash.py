import streamlit as st
import streamlit.components.v1 as components
st.set_page_config("Geometry dash by Debayan Das", page_icon="🏐")
dash = st.button('Geometry dash')
if dash:
  components.html("""
                <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Geometry Dash Dual Gravity (Hard Mode)</title>
<style>
  body { margin: 0; overflow: hidden; background: linear-gradient(to bottom, #001, #004); }
  canvas { display: block; margin: auto; background: linear-gradient(to top, #111, #000); }
</style>
</head>
<body>
<canvas id="game"></canvas>
<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let gravity = 0.8;
let cube = {
  x: 150,
  y: canvas.height - 150,
  size: 40,
  velocityY: 0,
  onGround: true,
  inverted: false
};

let groundHeight = 80;
let obstacles = [];
let speed = 10;

// --- Generate random varied obstacles ---
function generateObstacles() {
  let x = 600;
  for (let i = 0; i < 70; i++) {
    const type = Math.floor(Math.random() * 3); // 0: triangle, 1: block, 2: double spike
    const bottom = Math.random() > 0.5;
    const gap = 320 + Math.random() * 400;
    const color = bottom ? "#00ffff" : "#ffff00";
    const width = 50 + Math.random() * 40;
    const height = 60 + Math.random() * 80;

    obstacles.push({
      x,
      width,
      height,
      type,
      bottom,
      color
    });

    x += gap;
  }
}

generateObstacles();

function drawGround() {
  ctx.fillStyle = "#0a0";
  ctx.fillRect(0, canvas.height - groundHeight, canvas.width, groundHeight);
  ctx.fillRect(0, 0, canvas.width, groundHeight);
}

function drawCube() {
  ctx.fillStyle = "#f00";
  ctx.fillRect(cube.x, cube.y, cube.size, cube.size);
}

function drawObstacle(obs) {
  ctx.fillStyle = obs.color;
  if (obs.type === 0) {
    // Single triangle spike
    ctx.beginPath();
    if (obs.bottom) {
      ctx.moveTo(obs.x, canvas.height - groundHeight);
      ctx.lineTo(obs.x + obs.width / 2, canvas.height - groundHeight - obs.height);
      ctx.lineTo(obs.x + obs.width, canvas.height - groundHeight);
    } else {
      ctx.moveTo(obs.x, groundHeight);
      ctx.lineTo(obs.x + obs.width / 2, groundHeight + obs.height);
      ctx.lineTo(obs.x + obs.width, groundHeight);
    }
    ctx.closePath();
    ctx.fill();
  } 
  else if (obs.type === 1) {
    // Block
    if (obs.bottom) {
      ctx.fillRect(obs.x, canvas.height - groundHeight - obs.height, obs.width, obs.height);
    } else {
      ctx.fillRect(obs.x, groundHeight, obs.width, obs.height);
    }
  } 
  else if (obs.type === 2) {
    // Double spike
    const spacing = obs.width / 3;
    for (let i = 0; i < 2; i++) {
      ctx.beginPath();
      if (obs.bottom) {
        ctx.moveTo(obs.x + i * spacing, canvas.height - groundHeight);
        ctx.lineTo(obs.x + i * spacing + spacing / 2, canvas.height - groundHeight - obs.height);
        ctx.lineTo(obs.x + i * spacing + spacing, canvas.height - groundHeight);
      } else {
        ctx.moveTo(obs.x + i * spacing, groundHeight);
        ctx.lineTo(obs.x + i * spacing + spacing / 2, groundHeight + obs.height);
        ctx.lineTo(obs.x + i * spacing + spacing, groundHeight);
      }
      ctx.closePath();
      ctx.fill();
    }
  }
}

function updateCube() {
  cube.velocityY += cube.inverted ? -gravity : gravity;
  cube.y += cube.velocityY;

  let bottomGround = canvas.height - groundHeight - cube.size;
  let topGround = groundHeight;

  if (!cube.inverted && cube.y > bottomGround) {
    cube.y = bottomGround;
    cube.velocityY = 0;
    cube.onGround = true;
  } else if (cube.inverted && cube.y < topGround) {
    cube.y = topGround;
    cube.velocityY = 0;
    cube.onGround = true;
  }
}

function checkCollision() {
  for (let obs of obstacles) {
    let obsY = obs.bottom
      ? canvas.height - groundHeight - obs.height
      : groundHeight;
    let collides =
      cube.x < obs.x + obs.width &&
      cube.x + cube.size > obs.x &&
      cube.y < obsY + obs.height &&
      cube.y + cube.size > obsY;

    if (collides) {
      alert("Game Over!");
      document.location.reload();
    }
  }
}

function updateObstacles() {
  for (let obs of obstacles) obs.x -= speed;
}

function gameLoop() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawGround();
  updateCube();
  drawCube();

  for (let obs of obstacles) {
    drawObstacle(obs);
  }

  updateObstacles();
  checkCollision();

  requestAnimationFrame(gameLoop);
}

window.addEventListener("mousedown", () => {
  if (cube.onGround) {
    cube.inverted = !cube.inverted;
    cube.velocityY = cube.inverted ? -14 : 14;
    cube.onGround = false;
  }
});

gameLoop();
</script>
</body>
</html>
                """ , height=600)

  st.caption("Geometry Dash Dual Gravity (Hard Mode) by Debayan Das")
else:
  

