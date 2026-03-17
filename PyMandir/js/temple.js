/* ================================================
   Temple Module
   Draw the temple on canvas based on stage
   ================================================ */

const Temple = (() => {
    let canvas, ctx;

    function init(canvasEl) {
        canvas = canvasEl;
        ctx = canvas.getContext('2d');
        resize();
        window.addEventListener('resize', resize);
    }

    function resize() {
        const parent = canvas.parentElement;
        const w = Math.min(parent.clientWidth - 20, 500);
        const ratio = window.devicePixelRatio || 1;
        canvas.style.width = w + 'px';
        canvas.style.height = (w * 0.7) + 'px';
        canvas.width = w * ratio;
        canvas.height = (w * 0.7) * ratio;
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    function draw(stage, hasCracks) {
        const w = parseInt(canvas.style.width);
        const h = parseInt(canvas.style.height);
        ctx.clearRect(0, 0, w, h);

        // Ground line
        const groundY = h - 20;

        // Color palette
        const stoneColor = '#8b7355';
        const stoneDark = '#6b5740';
        const stoneLight = '#a89070';
        const goldAccent = '#c9a84c';
        const goldBright = '#e8c55a';
        const darkBg = '#1a1610';

        // Center x
        const cx = w / 2;

        // Draw ground
        ctx.fillStyle = '#3a3020';
        ctx.fillRect(0, groundY, w, 20);
        const grd = ctx.createLinearGradient(0, groundY, 0, groundY + 20);
        grd.addColorStop(0, '#5a4a30');
        grd.addColorStop(1, '#2a2015');
        ctx.fillStyle = grd;
        ctx.fillRect(0, groundY, w, 20);

        if (stage >= 1) drawFoundation(cx, groundY, w, stoneColor, stoneDark, stoneLight, goldAccent);
        if (stage >= 2) drawWalls(cx, groundY, stoneColor, stoneDark, stoneLight, goldAccent);
        if (stage >= 3) drawDoorway(cx, groundY, stoneColor, stoneDark, goldAccent, goldBright, darkBg);
        if (stage >= 4) drawCarvings(cx, groundY, goldAccent, goldBright);
        if (stage >= 5) drawShikhara(cx, groundY, stoneColor, stoneDark, stoneLight, goldAccent, goldBright);
        if (stage >= 6) drawFlags(cx, groundY, goldBright);

        if (hasCracks) drawCracks(cx, groundY, w);
    }

    function drawFoundation(cx, groundY, w, stone, dark, light, gold) {
        // Platform steps
        const steps = [
            { y: groundY - 8, width: 280, height: 10 },
            { y: groundY - 18, width: 250, height: 10 },
            { y: groundY - 28, width: 220, height: 10 },
        ];

        steps.forEach(s => {
            ctx.fillStyle = dark;
            ctx.fillRect(cx - s.width / 2, s.y, s.width, s.height);

            // Stone texture lines
            ctx.strokeStyle = stone;
            ctx.lineWidth = 0.5;
            for (let x = cx - s.width / 2; x < cx + s.width / 2; x += 20) {
                ctx.beginPath();
                ctx.moveTo(x, s.y);
                ctx.lineTo(x, s.y + s.height);
                ctx.stroke();
            }

            // Top highlight
            ctx.fillStyle = light;
            ctx.fillRect(cx - s.width / 2, s.y, s.width, 2);
        });

        // Gold trim on top step
        ctx.fillStyle = gold;
        ctx.fillRect(cx - 110, groundY - 30, 220, 2);
    }

    function drawWalls(cx, groundY, stone, dark, light, gold) {
        const baseY = groundY - 28;
        const wallH = 80;
        const wallW = 180;

        // Main walls
        ctx.fillStyle = stone;
        ctx.fillRect(cx - wallW / 2, baseY - wallH, wallW, wallH);

        // Stone brick pattern
        ctx.strokeStyle = dark;
        ctx.lineWidth = 0.8;
        for (let y = baseY - wallH; y < baseY; y += 12) {
            ctx.beginPath();
            ctx.moveTo(cx - wallW / 2, y);
            ctx.lineTo(cx + wallW / 2, y);
            ctx.stroke();

            const offset = (Math.floor((baseY - y) / 12) % 2) * 15;
            for (let x = cx - wallW / 2 + offset; x < cx + wallW / 2; x += 30) {
                ctx.beginPath();
                ctx.moveTo(x, y);
                ctx.lineTo(x, y + 12);
                ctx.stroke();
            }
        }

        // Side pillars
        [-1, 1].forEach(side => {
            const px = cx + side * (wallW / 2 - 5);
            ctx.fillStyle = dark;
            ctx.fillRect(px - 8, baseY - wallH - 5, 16, wallH + 5);
            ctx.fillStyle = light;
            ctx.fillRect(px - 6, baseY - wallH - 5, 12, wallH + 5);

            // Pillar cap
            ctx.fillStyle = gold;
            ctx.fillRect(px - 10, baseY - wallH - 10, 20, 6);
        });
    }

    function drawDoorway(cx, groundY, stone, dark, gold, goldBright, bg) {
        const baseY = groundY - 28;
        const doorW = 40;
        const doorH = 55;
        const doorX = cx - doorW / 2;
        const doorY = baseY - doorH;

        // Door opening
        ctx.fillStyle = bg;
        ctx.beginPath();
        ctx.moveTo(doorX, baseY);
        ctx.lineTo(doorX, doorY + 15);
        ctx.arc(cx, doorY + 15, doorW / 2, Math.PI, 0);
        ctx.lineTo(doorX + doorW, baseY);
        ctx.closePath();
        ctx.fill();

        // Door arch border
        ctx.strokeStyle = gold;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(doorX, baseY);
        ctx.lineTo(doorX, doorY + 15);
        ctx.arc(cx, doorY + 15, doorW / 2, Math.PI, 0);
        ctx.lineTo(doorX + doorW, baseY);
        ctx.stroke();

        // Steps to door
        for (let i = 0; i < 3; i++) {
            ctx.fillStyle = dark;
            ctx.fillRect(cx - 25 + i * 3, baseY + i * 4, 50 - i * 6, 4);
        }

        // Inner diya glow
        ctx.save();
        const glowGrd = ctx.createRadialGradient(cx, baseY - 20, 2, cx, baseY - 20, 30);
        glowGrd.addColorStop(0, 'rgba(245, 166, 35, 0.4)');
        glowGrd.addColorStop(1, 'transparent');
        ctx.fillStyle = glowGrd;
        ctx.fillRect(cx - 30, baseY - 50, 60, 40);
        ctx.restore();
    }

    function drawCarvings(cx, groundY, gold, goldBright) {
        const baseY = groundY - 28;

        // Decorative patterns on walls
        ctx.strokeStyle = gold;
        ctx.lineWidth = 1;

        // Lotus motifs
        [-1, 1].forEach(side => {
            const lx = cx + side * 55;
            const ly = baseY - 65;
            drawLotus(lx, ly, 12, gold);
        });

        // Diamond patterns
        [-1, 1].forEach(side => {
            const dx = cx + side * 55;
            const dy = baseY - 40;
            ctx.strokeStyle = goldBright;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(dx, dy - 8);
            ctx.lineTo(dx + 6, dy);
            ctx.lineTo(dx, dy + 8);
            ctx.lineTo(dx - 6, dy);
            ctx.closePath();
            ctx.stroke();
        });

        // Horizontal decorative band
        ctx.fillStyle = gold;
        ctx.fillRect(cx - 90, baseY - 83, 180, 3);

        // Small triangular patterns along the band
        for (let x = cx - 85; x < cx + 85; x += 12) {
            ctx.beginPath();
            ctx.moveTo(x, baseY - 80);
            ctx.lineTo(x + 6, baseY - 75);
            ctx.lineTo(x + 12, baseY - 80);
            ctx.strokeStyle = gold;
            ctx.lineWidth = 0.8;
            ctx.stroke();
        }
    }

    function drawLotus(x, y, r, color) {
        ctx.save();
        ctx.strokeStyle = color;
        ctx.lineWidth = 1;
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2;
            ctx.beginPath();
            ctx.ellipse(
                x + Math.cos(angle) * r * 0.4,
                y + Math.sin(angle) * r * 0.4,
                r * 0.5, r * 0.25,
                angle, 0, Math.PI * 2
            );
            ctx.stroke();
        }
        // Center circle
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.restore();
    }

    function drawShikhara(cx, groundY, stone, dark, light, gold, goldBright) {
        const baseY = groundY - 28 - 80; // top of walls

        // Shikhara (tower/dome)
        ctx.fillStyle = stone;
        ctx.beginPath();
        ctx.moveTo(cx - 70, baseY - 5);

        // Curved tower shape
        ctx.bezierCurveTo(
            cx - 65, baseY - 40,
            cx - 40, baseY - 90,
            cx, baseY - 120
        );
        ctx.bezierCurveTo(
            cx + 40, baseY - 90,
            cx + 65, baseY - 40,
            cx + 70, baseY - 5
        );
        ctx.closePath();
        ctx.fill();

        // Horizontal ridges on shikhara
        ctx.strokeStyle = dark;
        ctx.lineWidth = 1;
        for (let y = baseY - 10; y > baseY - 110; y -= 8) {
            const progress = (baseY - y) / 120;
            const width = 70 * (1 - progress * 0.85);
            ctx.beginPath();
            ctx.moveTo(cx - width, y);
            ctx.lineTo(cx + width, y);
            ctx.stroke();
        }

        // Top kalash (golden pot)
        ctx.fillStyle = goldBright;
        ctx.beginPath();
        ctx.arc(cx, baseY - 120, 6, 0, Math.PI * 2);
        ctx.fill();

        // Spire on top
        ctx.strokeStyle = goldBright;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(cx, baseY - 126);
        ctx.lineTo(cx, baseY - 140);
        ctx.stroke();

        // Trident on top
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(cx - 6, baseY - 137);
        ctx.lineTo(cx, baseY - 145);
        ctx.lineTo(cx + 6, baseY - 137);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(cx, baseY - 140);
        ctx.lineTo(cx, baseY - 145);
        ctx.stroke();
    }

    function drawFlags(cx, groundY) {
        const baseY = groundY - 28 - 80;

        // Flags on sides
        [-1, 1].forEach(side => {
            const fx = cx + side * 95;
            const fy = baseY + 10;

            // Flag pole
            ctx.strokeStyle = '#c9a84c';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(fx, fy + 30);
            ctx.lineTo(fx, fy - 40);
            ctx.stroke();

            // Flag (animated feel with waviness)
            ctx.fillStyle = '#c0593a';
            ctx.beginPath();
            ctx.moveTo(fx, fy - 40);
            ctx.quadraticCurveTo(fx + side * 15, fy - 35, fx + side * 25, fy - 30);
            ctx.quadraticCurveTo(fx + side * 15, fy - 25, fx, fy - 22);
            ctx.closePath();
            ctx.fill();

            // Gold trim on flag
            ctx.strokeStyle = '#e8c55a';
            ctx.lineWidth = 0.8;
            ctx.stroke();
        });

        // Small diyas at base
        [-1, 1].forEach(side => {
            const dx = cx + side * 70;
            const dy = groundY - 30;
            ctx.fillStyle = '#c9a84c';
            ctx.beginPath();
            ctx.ellipse(dx, dy, 5, 3, 0, 0, Math.PI * 2);
            ctx.fill();

            // Flame
            ctx.fillStyle = '#f5a623';
            ctx.beginPath();
            ctx.ellipse(dx, dy - 5, 2, 4, 0, 0, Math.PI * 2);
            ctx.fill();

            // Glow
            ctx.save();
            const glowG = ctx.createRadialGradient(dx, dy - 5, 1, dx, dy - 5, 15);
            glowG.addColorStop(0, 'rgba(245, 166, 35, 0.3)');
            glowG.addColorStop(1, 'transparent');
            ctx.fillStyle = glowG;
            ctx.fillRect(dx - 15, dy - 20, 30, 25);
            ctx.restore();
        });
    }

    function drawCracks(cx, groundY, w) {
        ctx.strokeStyle = '#5a2a1a';
        ctx.lineWidth = 2;

        // Crack 1
        ctx.beginPath();
        ctx.moveTo(cx - 40, groundY - 60);
        ctx.lineTo(cx - 35, groundY - 70);
        ctx.lineTo(cx - 45, groundY - 80);
        ctx.lineTo(cx - 38, groundY - 90);
        ctx.stroke();

        // Crack 2
        ctx.beginPath();
        ctx.moveTo(cx + 30, groundY - 50);
        ctx.lineTo(cx + 38, groundY - 65);
        ctx.lineTo(cx + 32, groundY - 75);
        ctx.stroke();

        // Crack 3
        ctx.beginPath();
        ctx.moveTo(cx - 10, groundY - 35);
        ctx.lineTo(cx - 5, groundY - 45);
        ctx.lineTo(cx - 15, groundY - 52);
        ctx.stroke();

        // Rubble pieces
        ctx.fillStyle = '#6b5740';
        [
            { x: cx - 50, y: groundY - 25 },
            { x: cx + 45, y: groundY - 22 },
            { x: cx - 30, y: groundY - 20 },
        ].forEach(p => {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p.x + 8, p.y - 3);
            ctx.lineTo(p.x + 10, p.y + 4);
            ctx.lineTo(p.x + 2, p.y + 5);
            ctx.closePath();
            ctx.fill();
        });
    }

    return { init, draw, resize };
})();
