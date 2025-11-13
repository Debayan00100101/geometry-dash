import streamlit as st
import streamlit.components.v1 as components
st.set_page_config("Geometry dash by Debayan Das", page_icon="🏐")
st.title('Wanna play!')
dash = st.button('Geometry dash')
max = st.button("bedwars")
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
elif max:
  components.html("""
  <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Minecraft-Style BedWars 4-Teams</title>
<style>
  body { margin: 0; overflow: hidden; background: black; }
  canvas { display: block; margin: auto; background: url('/Screenshot 2025-10-06 130003.png'); }
  #resultBox {
    position: absolute;
    top: 40%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 60px;
    color: white;
    font-family: Arial, sans-serif;
    background: rgba(0,0,0,0.7);
    padding: 40px 80px;
    border-radius: 20px;
    display: none;
    text-align: center;
  }
</style>
</head>
<body>
<canvas id="gameCanvas" width="900" height="500"></canvas>
<div id="resultBox"></div>
<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const resultBox = document.getElementById("resultBox");

const keys = {};
document.addEventListener("keydown", e => keys[e.key.toLowerCase()] = true);
document.addEventListener("keyup", e => keys[e.key.toLowerCase()] = false);

let mouse = {x: 0, y: 0, left: false, right: false};
canvas.addEventListener("mousedown", e => {
  if (e.button === 0) mouse.left = true;
  if (e.button === 2) mouse.right = true;
});
canvas.addEventListener("mouseup", e => {
  if (e.button === 0) mouse.left = false;
  if (e.button === 2) mouse.right = false;
});
canvas.addEventListener("contextmenu", e => e.preventDefault());
canvas.addEventListener("mousemove", e => {
  const rect = canvas.getBoundingClientRect();
  mouse.x = e.clientX - rect.left;
  mouse.y = e.clientY - rect.top;
});

const gravity = 0.7, friction = 0.85;

// ---- Player ----
class Player {
  constructor(x, y, color, team) {
    this.x = x; this.y = y;
    this.w = 30; this.h = 40;
    this.velX = 0; this.velY = 0;
    this.color = color; this.team = team;
    this.health = 100; this.onGround = false; this.alive = true;
    this.lastHit = 0;
  }
  update(platforms) {
    if (!this.alive) return;
    this.velY += gravity;
    this.x += this.velX;
    this.y += this.velY;
    this.onGround = false;

    // stop above top
    if (this.y < 0) {
      this.y = 0;
      if (this.velY < 0) this.velY = 0;
    }

    for (let p of platforms) {
      if (this.x + this.w > p.x && this.x < p.x + p.w &&
          this.y + this.h > p.y && this.y + this.h < p.y + p.h) {
        this.y = p.y - this.h;
        this.velY = 0;
        this.onGround = true;
      }
    }

    if (this.y > canvas.height + 200) this.respawn();
    this.velX *= friction;
  }
  draw(camX) {
    if (!this.alive) return;
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x - camX, this.y, this.w, this.h);
    ctx.fillStyle = "white";
    ctx.font = "12px Arial";
    ctx.fillText(Math.floor(this.health), this.x - camX + 6, this.y - 5);
  }
  respawn() {
    const bed = beds.find(b => b.team === this.team);
    if (bed && !bed.destroyed) {
      this.health = 100;
      this.x = bed.x; this.y = bed.y - 50;
      this.velX = this.velY = 0;
    } else {
      this.alive = false;
      console.log(`${this.team.toUpperCase()} player eliminated!`);
      checkTeamAlive(this.team);
      checkGameOver();
    }
  }
}

// ---- Platform ----
class Platform {
  constructor(x, y, w, h, color="#654321") {
    this.x = x; this.y = y; this.w = w; this.h = h; this.color = color;
  }
  draw(camX) {
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x - camX, this.y, this.w, this.h);
  }
}

// ---- Bed ----
class Bed {
  constructor(x, y, team, color) {
    this.x = x; this.y = y; this.w = 40; this.h = 20;
    this.team = team; this.color = color; this.health = 100;
    this.destroyed = false;
  }
  draw(camX) {
    if (this.destroyed) return;
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x - camX, this.y, this.w, this.h);
    ctx.fillStyle = "white";
    ctx.font = "10px Arial";
    ctx.fillText("Bed", this.x - camX + 5, this.y + 14);
  }
}

const platforms = [
  new Platform(200, 400, 150, 20),
  new Platform(500, 400, 150, 20),
  new Platform(800, 400, 150, 20),
  new Platform(-100, 400, 150, 20)
];
const beds = [
  new Bed(210, 380, "red", "red"),
  new Bed(510, 380, "blue", "blue"),
  new Bed(810, 380, "green", "green"),
  new Bed(-90, 380, "yellow", "yellow")
];
const players = [
  new Player(220, 360, "red", "red"), // YOU
  new Player(520, 360, "blue", "blue"),
  new Player(820, 360, "green", "green"),
  new Player(-80, 360, "yellow", "yellow")
];
const player = players[0];
let blocks = [];

// ---- Mechanics ----
function placeBlock() {
  blocks.push(new Platform(mouse.x + camX - 10, mouse.y - 10, 20, 20, "#a0522d"));
}
function breakBlock() {
  const reach = 60;
  for (let i = 0; i < blocks.length; i++) {
    const b = blocks[i];
    const dx = (player.x + player.w / 2) - (b.x + b.w / 2);
    const dy = (player.y + player.h / 2) - (b.y + b.h / 2);
    const dist = Math.sqrt(dx * dx + dy * dy);
    const mouseDist = Math.sqrt((mouse.x + camX - (b.x + b.w/2))**2 + (mouse.y - (b.y + b.h/2))**2);
    if (dist < reach && mouseDist < 40) {
      blocks.splice(i, 1);
      break;
    }
  }
}

function checkTeamAlive(team) {
  const teamPlayers = players.filter(p => p.team === team && p.alive);
  if (teamPlayers.length === 0) {
    console.log(`❌ ${team.toUpperCase()} team eliminated!`);
  } else {
    console.log(`${team.toUpperCase()} team has ${teamPlayers.length} player(s) left.`);
  }
}

function tryBreakBed(attacker) {
  for (let bed of beds) {
    if (bed.destroyed || bed.team === attacker.team) continue;
    const dx = attacker.x - bed.x, dy = attacker.y - bed.y;
    if (Math.hypot(dx,dy) < 60) { 
      bed.health -= 2; 
      if (bed.health <= 0 && !bed.destroyed) {
        bed.destroyed = true;
        console.log(`⚠ ${bed.team.toUpperCase()} team's bed destroyed!`);
        const aliveCount = players.filter(p => p.team === bed.team && p.alive).length;
        console.log(`${bed.team.toUpperCase()} team players left: ${aliveCount}`);
        checkGameOver();
      }
    }
  }
}

function attack(attacker, target) {
  if (!attacker.alive || !target.alive) return;
  const now = Date.now();
  if (now - attacker.lastHit < 500) return;
  const dx = attacker.x - target.x, dy = attacker.y - target.y;
  if (Math.hypot(dx,dy) < 60) {
    target.health -= 10;
    target.velY = -8;
    target.velX = dx > 0 ? -5 : 5;
    attacker.lastHit = now;
    if (target.health <= 0) target.respawn();
  }
}

// ---- WIN / LOSE ----
function checkGameOver() {
  const myBed = beds.find(b => b.team === player.team);
  const myAlive = player.alive;

  const otherTeams = beds.filter(b => b.team !== player.team);
  const otherAlivePlayers = players.filter(p => p.team !== player.team && p.alive).length;
  const otherAliveBeds = otherTeams.filter(b => !b.destroyed).length;

  if (!myAlive && myBed.destroyed) {
    showResult("YOU LOSE");
  } 
  else if (otherAlivePlayers === 0 && otherAliveBeds === 0 && myAlive) {
    showResult("YOU WIN");
  }
}

function showResult(text) {
  resultBox.innerText = text;
  resultBox.style.display = "block";
  setTimeout(() => location.reload(), 5000);
}

// ---- AI ----
function smartAI(p) {
  if (!p.alive) return;
  const enemies = players.filter(pl => pl !== p && pl.alive);
  if (enemies.length === 0) return;
  const target = enemies[Math.floor(Math.random() * enemies.length)];
  const targetBed = beds.find(b => b.team === target.team);

  let goalX = targetBed && !targetBed.destroyed ? targetBed.x : target.x;
  if (goalX < p.x - 10) p.velX = -2.5;
  else if (goalX > p.x + 10) p.velX = 2.5;
  else p.velX = 0;

  if (p.onGround && Math.random() < 0.03) p.velY = -12;
  if (Math.random() < 0.01) blocks.push(new Platform(p.x, p.y + p.h, 20, 20, "#8B4513"));

  const dx = target.x - p.x, dy = target.y - p.y;
  if (Math.hypot(dx,dy) < 60) attack(p, target);
  if (targetBed && !targetBed.destroyed && Math.hypot(p.x - targetBed.x, p.y - targetBed.y) < 60)
    tryBreakBed(p);
}

// ---- Camera ----
let camX = 0;

// ---- Main Loop ----
function update() {
  if (player.alive) {
    let moveSpeed = 4;
    if (keys["a"]) player.velX = -moveSpeed;
    if (keys["d"]) player.velX = moveSpeed;
    if (keys[" "] && player.onGround) player.velY = -14;
    if (keys["f"]) players.forEach(p => p !== player && attack(player, p));
    if (keys["e"]) tryBreakBed(player);
  }
  if (mouse.left) placeBlock();
  if (mouse.right) breakBlock();

  for (let p of players) {
    p.update([...platforms, ...blocks]);
    if (p !== player) smartAI(p);
  }

  camX += ((player.x - canvas.width / 2) - camX) * 0.1;
  checkGameOver();
}

function draw() {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  for (let p of [...platforms, ...blocks]) p.draw(camX);
  for (let b of beds) b.draw(camX);
  for (let p of players) p.draw(camX);

  const aliveBeds = beds.filter(b => !b.destroyed).length;
  ctx.fillStyle = "rgba(0,0,0,0.5)";
  ctx.fillRect(10, 10, 240, 160);
  ctx.fillStyle = "white";
  ctx.font = "14px Arial";
  ctx.fillText("Team Status:", 20, 30);
  beds.forEach((b, i) => {
    const teamPlayers = players.filter(p => p.team === b.team && p.alive).length;
    ctx.fillStyle = b.destroyed ? "gray" : b.color;
    ctx.fillText(`${b.team.toUpperCase()}: Bed ${b.destroyed ? "❌" : "✅"} | Players: ${teamPlayers}`, 20, 50 + i*20);
  });
  ctx.fillStyle = "yellow";
  ctx.fillText(`Beds Left: ${aliveBeds}`, 20, 50 + beds.length*20 + 5);
  ctx.fillStyle = "white";
  ctx.fillText("A/D=Move  Space=Jump  F=Attack  E=Break Bed",10,canvas.height-10);
}

function loop() { update(); draw(); requestAnimationFrame(loop); }
loop();
</script>
</body>
</html>

  """, height=600)
  st.caption("bedwars, controls are for pc only... play & have a fun -from debayan")





