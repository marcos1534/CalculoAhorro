def get_pacman_game():
    return """
    <!DOCTYPE html>
    <html>
    <head><style>
        body { background-color: #000; color: white; display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }
        canvas { border: 4px solid #1919A6; box-shadow: 0 0 20px rgba(25, 25, 166, 0.8); background-color: #000; }
        h3 { color: #FFFF00; text-shadow: 2px 2px #ff0000; }
        .controls { margin-top: 10px; color: #aaa; }
    </style></head>
    <body>
    <h3>🟡 WAKA WAKA (Pac-Man Style)</h3>
    <div id="score">SCORE: 0</div>
    <canvas id="gc" width="400" height="400"></canvas>
    <div class="controls">Usa las FLECHAS del teclado</div>
    <script>
    const canvas = document.getElementById("gc");
    const ctx = canvas.getContext("2d");
    const tileSize = 20;
    const tileCount = 20;
    let score = 0;
    
    let pacman = { x: 10, y: 10, dx: 0, dy: 0, mouth: 0.2, mouthDir: 1 };
    let ghosts = [
        { x: 1, y: 1, color: "red", dx: 1, dy: 0 },
        { x: 18, y: 1, color: "pink", dx: 0, dy: 1 },
        { x: 1, y: 18, color: "cyan", dx: 0, dy: -1 },
        { x: 18, y: 18, color: "orange", dx: -1, dy: 0 }
    ];
    let food = [];
    
    // Generar comida simple
    for(let i=0; i<tileCount; i++){
        for(let j=0; j<tileCount; j++){
            if(Math.random() > 0.1) food.push({x:i, y:j});
        }
    }

    document.addEventListener("keydown", (e) => {
        if(e.keyCode == 37) { pacman.dx = -1; pacman.dy = 0; }
        if(e.keyCode == 38) { pacman.dx = 0; pacman.dy = -1; }
        if(e.keyCode == 39) { pacman.dx = 1; pacman.dy = 0; }
        if(e.keyCode == 40) { pacman.dx = 0; pacman.dy = 1; }
    });

    function update() {
        // Mover Pacman
        pacman.x += pacman.dx;
        pacman.y += pacman.dy;
        
        // Paredes (wrap around)
        if(pacman.x < 0) pacman.x = tileCount-1;
        if(pacman.x >= tileCount) pacman.x = 0;
        if(pacman.y < 0) pacman.y = tileCount-1;
        if(pacman.y >= tileCount) pacman.y = 0;

        // Comer
        for(let i=0; i<food.length; i++){
            if(food[i].x === pacman.x && food[i].y === pacman.y){
                score += 10;
                food.splice(i, 1);
                document.getElementById("score").innerText = "SCORE: " + score;
            }
        }

        // Mover Fantasmas (IA básica aleatoria)
        ghosts.forEach(g => {
            if(Math.random() < 0.05) {
                const dirs = [{x:1,y:0}, {x:-1,y:0}, {x:0,y:1}, {x:0,y:-1}];
                const d = dirs[Math.floor(Math.random()*4)];
                g.dx = d.x; g.dy = d.y;
            }
            g.x += g.dx; g.y += g.dy;
            
            // Limites fantasmas
            if(g.x < 0) g.x = tileCount-1; if(g.x >= tileCount) g.x = 0;
            if(g.y < 0) g.y = tileCount-1; if(g.y >= tileCount) g.y = 0;

            // Colisión
            if(Math.round(g.x) === pacman.x && Math.round(g.y) === pacman.y) {
                pacman.x = 10; pacman.y = 10; pacman.dx=0; pacman.dy=0;
                score = 0; document.getElementById("score").innerText = "SCORE: " + score + " (MUERTO)";
            }
        });
    }

    function draw() {
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Comida
        ctx.fillStyle = "#FFB897";
        food.forEach(f => {
            ctx.fillRect(f.x*tileSize + 8, f.y*tileSize + 8, 4, 4);
        });

        // Pacman
        ctx.fillStyle = "yellow";
        ctx.beginPath();
        let angle = 0;
        if(pacman.dx === 1) angle = 0;
        if(pacman.dx === -1) angle = Math.PI;
        if(pacman.dy === -1) angle = -Math.PI/2;
        if(pacman.dy === 1) angle = Math.PI/2;
        
        ctx.arc(pacman.x*tileSize + tileSize/2, pacman.y*tileSize + tileSize/2, tileSize/2 - 2, angle + 0.2, angle + 2 * Math.PI - 0.2);
        ctx.lineTo(pacman.x*tileSize + tileSize/2, pacman.y*tileSize + tileSize/2);
        ctx.fill();

        // Fantasmas
        ghosts.forEach(g => {
            ctx.fillStyle = g.color;
            ctx.beginPath();
            let gx = g.x*tileSize; let gy = g.y*tileSize;
            ctx.arc(gx + 10, gy + 10, 8, Math.PI, 0);
            ctx.lineTo(gx + 20, gy + 20);
            ctx.lineTo(gx + 0, gy + 20);
            ctx.fill();
            // Ojos
            ctx.fillStyle = "white";
            ctx.beginPath(); ctx.arc(gx + 6, gy + 8, 3, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(gx + 14, gy + 8, 3, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "blue";
            ctx.beginPath(); ctx.arc(gx + 6, gy + 8, 1.5, 0, Math.PI*2); ctx.fill();
            ctx.beginPath(); ctx.arc(gx + 14, gy + 8, 1.5, 0, Math.PI*2); ctx.fill();
        });
    }

    setInterval(() => { update(); draw(); }, 1000/10);
    </script></body></html>
    """

def get_tetris_game():
    return """
    <!DOCTYPE html>
    <html>
    <head><style>
        body { background: #202028; color: #fff; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; }
        canvas { border: 2px solid #fff; box-shadow: 0 0 20px rgba(255,255,255,0.2); }
        h3 { color: #a966ff; }
    </style></head>
    <body>
    <h3>🧱 TETRIS</h3>
    <div id="score">Score: 0</div>
    <canvas id="tetris" width="240" height="400"></canvas>
    <div style="font-size:12px; margin-top:10px;">Flechas: Mover/Rotar | Abajo: Caer</div>
    <script>
    const canvas = document.getElementById('tetris');
    const context = canvas.getContext('2d');
    context.scale(20, 20);
    function arenaSweep() {
        let rowCount = 1;
        outer: for (let y = arena.length -1; y > 0; --y) {
            for (let x = 0; x < arena[y].length; ++x) {
                if (arena[y][x] === 0) continue outer;
            }
            const row = arena.splice(y, 1)[0].fill(0);
            arena.unshift(row);
            ++y;
            player.score += rowCount * 10;
            rowCount *= 2;
        }
    }
    function collide(arena, player) {
        const m = player.matrix; const o = player.pos;
        for (let y = 0; y < m.length; ++y) {
            for (let x = 0; x < m[y].length; ++x) {
                if (m[y][x] !== 0 && (arena[y + o.y] && arena[y + o.y][x + o.x]) !== 0) return true;
            }
        }
        return false;
    }
    function createMatrix(w, h) {
        const matrix = [];
        while (h--) matrix.push(new Array(w).fill(0));
        return matrix;
    }
    function createPiece(type) {
        if (type === 'I') return [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]];
        if (type === 'L') return [[0,2,0],[0,2,0],[0,2,2]];
        if (type === 'J') return [[0,3,0],[0,3,0],[3,3,0]];
        if (type === 'O') return [[4,4],[4,4]];
        if (type === 'Z') return [[5,5,0],[0,5,5],[0,0,0]];
        if (type === 'S') return [[0,6,6],[6,6,0],[0,0,0]];
        if (type === 'T') return [[0,7,0],[7,7,7],[0,0,0]];
    }
    function draw() {
        context.fillStyle = '#000'; context.fillRect(0, 0, canvas.width, canvas.height);
        drawMatrix(arena, {x: 0, y: 0});
        drawMatrix(player.matrix, player.pos);
    }
    function drawMatrix(matrix, offset) {
        matrix.forEach((row, y) => {
            row.forEach((value, x) => {
                if (value !== 0) {
                    context.fillStyle = colors[value];
                    context.fillRect(x + offset.x, y + offset.y, 1, 1);
                }
            });
        });
    }
    function merge(arena, player) {
        player.matrix.forEach((row, y) => {
            row.forEach((value, x) => { if (value !== 0) arena[y + player.pos.y][x + player.pos.x] = value; });
        });
    }
    function playerDrop() {
        player.pos.y++;
        if (collide(arena, player)) {
            player.pos.y--; merge(arena, player); playerReset(); arenaSweep(); updateScore();
        }
        dropCounter = 0;
    }
    function playerMove(dir) {
        player.pos.x += dir;
        if (collide(arena, player)) player.pos.x -= dir;
    }
    function playerReset() {
        const pieces = 'ILJOTSZ';
        player.matrix = createPiece(pieces[pieces.length * Math.random() | 0]);
        player.pos.y = 0; player.pos.x = (arena[0].length / 2 | 0) - (player.matrix[0].length / 2 | 0);
        if (collide(arena, player)) { arena.forEach(row => row.fill(0)); player.score = 0; updateScore(); }
    }
    function playerRotate(dir) {
        const pos = player.pos.x;
        let offset = 1;
        rotate(player.matrix, dir);
        while (collide(arena, player)) {
            player.pos.x += offset; offset = -(offset + (offset > 0 ? 1 : -1));
            if (offset > player.matrix[0].length) { rotate(player.matrix, -dir); player.pos.x = pos; return; }
        }
    }
    function rotate(matrix, dir) {
        for (let y = 0; y < matrix.length; ++y) {
            for (let x = 0; x < y; ++x) { [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]]; }
        }
        if (dir > 0) matrix.forEach(row => row.reverse()); else matrix.reverse();
    }
    let dropCounter = 0; let dropInterval = 1000; let lastTime = 0;
    function update(time = 0) {
        const deltaTime = time - lastTime; lastTime = time; dropCounter += deltaTime;
        if (dropCounter > dropInterval) playerDrop();
        draw(); requestAnimationFrame(update);
    }
    function updateScore() { document.getElementById('score').innerText = "Score: " + player.score; }
    const colors = [null, '#FF0D72', '#0DC2FF', '#0DFF72', '#F538FF', '#FF8E0D', '#FFE138', '#3877FF'];
    const arena = createMatrix(12, 20);
    const player = { pos: {x: 0, y: 0}, matrix: null, score: 0 };
    document.addEventListener('keydown', event => {
        if (event.keyCode === 37) playerMove(-1);
        else if (event.keyCode === 39) playerMove(1);
        else if (event.keyCode === 40) playerDrop();
        else if (event.keyCode === 81) playerRotate(-1);
        else if (event.keyCode === 87 || event.keyCode === 38) playerRotate(1);
    });
    playerReset(); updateScore(); update();
    </script></body></html>
    """

def get_space_invaders():
    return """
    <!DOCTYPE html>
    <html>
    <head><style>
        body { background-color: #000; color: #0f0; display: flex; flex-direction: column; align-items: center; font-family: 'Courier New', monospace; }
        canvas { border-bottom: 2px solid #0f0; background: url('https://www.transparenttextures.com/patterns/stardust.png'); }
        h3 { color: #0f0; margin-bottom:5px;}
    </style></head>
    <body>
    <h3>👾 SPACE INVADERS</h3>
    <div id="score">SCORE: 0000</div>
    <canvas id="game" width="400" height="400"></canvas>
    <script>
    const canvas = document.getElementById('game'); const ctx = canvas.getContext('2d');
    let score = 0;
    let player = {x: 180, y: 370, w: 20, h: 10, bullets: []};
    let enemies = [];
    let enemyDir = 1;
    let gameOver = false;

    // Crear enemigos pixel art (simulado)
    for(let r=0; r<4; r++){
        for(let c=0; c<8; c++){
            enemies.push({x: 30 + c*40, y: 30 + r*30, w: 20, h: 15, alive: true, type: r});
        }
    }

    document.addEventListener('keydown', e => {
        if(e.key === 'ArrowLeft') player.x -= 15;
        if(e.key === 'ArrowRight') player.x += 15;
        if(e.key === ' ' && player.bullets.length < 3) player.bullets.push({x: player.x + 9, y: player.y});
    });

    function drawAlien(x, y, type) {
        ctx.fillStyle = type == 0 ? '#ff0000' : (type == 1 ? '#00ff00' : '#ffff00');
        // Simular forma alien
        ctx.fillRect(x+4, y, 12, 15);
        ctx.fillRect(x, y+4, 20, 8);
        ctx.fillRect(x, y+15, 4, 4);
        ctx.fillRect(x+16, y+15, 4, 4);
        // Ojos
        ctx.fillStyle = 'black';
        ctx.fillRect(x+5, y+6, 3, 3); ctx.fillRect(x+12, y+6, 3, 3);
    }

    function loop() {
        if(gameOver) { ctx.fillStyle='white'; ctx.fillText("GAME OVER", 170, 200); return; }
        ctx.clearRect(0,0,400,400);

        // Player (Cañón)
        ctx.fillStyle = '#0f0';
        ctx.fillRect(player.x, player.y, player.w, player.h);
        ctx.fillRect(player.x + 8, player.y - 5, 4, 5);

        // Bullets
        ctx.fillStyle = 'white';
        player.bullets.forEach((b, i) => {
            b.y -= 5;
            ctx.fillRect(b.x, b.y, 2, 8);
            if(b.y < 0) player.bullets.splice(i, 1);
        });

        // Enemies
        let moveDown = false;
        let rightEdge = 0; let leftEdge = 400;
        
        enemies.forEach(e => {
            if(!e.alive) return;
            drawAlien(e.x, e.y, e.type);
            
            // Colisión balas
            player.bullets.forEach((b, bi) => {
                if(b.x > e.x && b.x < e.x+e.w && b.y > e.y && b.y < e.y+e.h) {
                    e.alive = false; player.bullets.splice(bi, 1); score+=100;
                    document.getElementById('score').innerText = "SCORE: " + score;
                }
            });

            if(e.x > rightEdge) rightEdge = e.x;
            if(e.x < leftEdge) leftEdge = e.x;
        });

        // Movimiento en bloque
        if(rightEdge > 370 && enemyDir === 1) { enemyDir = -1; moveDown = true; }
        if(leftEdge < 10 && enemyDir === -1) { enemyDir = 1; moveDown = true; }

        enemies.forEach(e => {
            if(e.alive) {
                e.x += enemyDir * 0.5;
                if(moveDown) e.y += 10;
                if(e.y > 350) gameOver = true;
            }
        });

        requestAnimationFrame(loop);
    }
    loop();
    </script></body></html>
    """

def get_donkey_kong():
    return """
    <!DOCTYPE html>
    <html>
    <head><style>
        body { background: #000; color: white; display: flex; flex-direction: column; align-items: center; font-family: sans-serif; }
        canvas { border: 2px solid #55f; background-color: #000; }
        h3 { color: #f0f; margin-bottom:5px; }
    </style></head>
    <body>
    <h3>🦍 KONG CLIMBER</h3>
    <div id="msg">Sube las escaleras!</div>
    <canvas id="cvs" width="400" height="500"></canvas>
    <script>
    const ctx = document.getElementById('cvs').getContext('2d');
    
    let mario = {x: 20, y: 450, w: 15, h: 20, climbing: false};
    let barrels = [];
    let score = 0;
    
    // Plataformas (Hierros)
    let platforms = [
        {x: 0, y: 470, w: 400},
        {x: 0, y: 370, w: 350}, // Nivel 2 (hueco derecha)
        {x: 50, y: 270, w: 350}, // Nivel 3 (hueco izquierda)
        {x: 0, y: 170, w: 350}, // Nivel 4
        {x: 150, y: 70, w: 100}  // Meta
    ];
    
    // Escaleras
    let ladders = [
        {x: 300, y: 370, h: 100},
        {x: 100, y: 270, h: 100},
        {x: 300, y: 170, h: 100},
        {x: 180, y: 70, h: 100}
    ];

    document.addEventListener('keydown', e => {
        if(e.key === 'ArrowRight') mario.x += 5;
        if(e.key === 'ArrowLeft') mario.x -= 5;
        if(e.key === 'ArrowUp') checkClimb(-5);
        if(e.key === 'ArrowDown') checkClimb(5);
    });

    function checkClimb(dy) {
        // Simple lógica de escaleras
        ladders.forEach(l => {
            if(mario.x > l.x - 10 && mario.x < l.x + 20) {
                 if(mario.y + dy < l.y + l.h && mario.y + dy > l.y - 20) mario.y += dy;
            }
        });
    }

    function spawnBarrel() {
        barrels.push({x: 50, y: 70, dx: 3, dy: 0, falling: false});
    }
    setInterval(spawnBarrel, 2500);

    function loop() {
        ctx.clearRect(0,0,400,500);
        
        // Dibujar Plataformas (Rojo DK style)
        ctx.fillStyle = '#b00';
        platforms.forEach(p => ctx.fillRect(p.x, p.y, p.w, 10));

        // Dibujar Escaleras (Azul)
        ctx.fillStyle = '#55f';
        ladders.forEach(l => {
            for(let i=0; i<l.h; i+=10) ctx.fillRect(l.x, l.y + i, 20, 2);
            ctx.fillRect(l.x, l.y, 2, l.h);
            ctx.fillRect(l.x+18, l.y, 2, l.h);
        });

        // Dibujar Mario
        ctx.fillStyle = 'red';
        ctx.fillRect(mario.x, mario.y, mario.w, mario.h);
        ctx.fillStyle = 'blue'; // peto
        ctx.fillRect(mario.x, mario.y+12, mario.w, 8);

        // Dibujar Kong
        ctx.fillStyle = '#630';
        ctx.fillRect(20, 40, 50, 50); // Kong body
        ctx.fillStyle = '#fa0';
        ctx.fillText("DK", 35, 65);

        // Dibujar Princesa
        ctx.fillStyle = 'pink';
        ctx.fillRect(190, 40, 15, 30);

        // Lógica Barriles
        ctx.fillStyle = '#963'; // marrón barril
        barrels.forEach((b, i) => {
            // Dibujar (círculo)
            ctx.beginPath(); ctx.arc(b.x, b.y+5, 8, 0, 7); ctx.fill();
            
            // Gravedad básica
            let onPlatform = false;
            platforms.forEach(p => {
                if(b.y >= p.y - 10 && b.y <= p.y + 5 && b.x > p.x && b.x < p.x + p.w) {
                    onPlatform = true;
                    b.y = p.y - 10;
                }
            });

            if(!onPlatform) {
                b.y += 3; // Caer
            } else {
                b.x += b.dx;
                // Rebotar en bordes o caer
                if(b.x > 390 || b.x < 10) b.dx *= -1;
            }
            
            // Colisión Mario
            let dx = mario.x - b.x; let dy = mario.y - b.y;
            let dist = Math.sqrt(dx*dx + dy*dy);
            if(dist < 15) {
                mario.x = 20; mario.y = 450;
                document.getElementById('msg').innerText = "OUCH! Intenta de nuevo";
            }
            
            if(b.y > 500) barrels.splice(i, 1);
        });
        
        // Win condition
        if(mario.y < 80 && mario.x > 150) {
            document.getElementById('msg').innerText = "¡GANASTE! RESCATASTE A LA PRINCESA";
        }

        requestAnimationFrame(loop);
    }
    loop();
    </script></body></html>
    """