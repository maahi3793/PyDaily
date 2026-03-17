/* ================================================
   Diya Module — 3D Oil Lamp
   Premium canvas-rendered diya with:
   - 3D shading, highlights, and cast shadows
   - Smooth flickering flame that shrinks with oil
   - Visible oil drain animation
   - Break mode: character refilling oil
   ================================================ */

const Diya = (() => {
    let focusCanvas, focusCtx;
    let breakCanvas, breakCtx;
    let animFrame;
    let oilLevel = 1;       // 1 = full, 0 = empty
    let targetOilLevel = 1;
    let flameTime = 0;
    let running = false;

    // Canvas sizing — bigger for detail
    const W = 500;
    const H = 550;

    function initFocus(canvasEl) {
        focusCanvas = canvasEl;
        focusCtx = canvasEl.getContext('2d');
        setupCanvas(canvasEl);
    }

    function initBreak(canvasEl) {
        breakCanvas = canvasEl;
        breakCtx = canvasEl.getContext('2d');
        setupCanvas(canvasEl);
    }

    function setupCanvas(canvasEl) {
        const ratio = window.devicePixelRatio || 1;
        canvasEl.style.width = W + 'px';
        canvasEl.style.height = H + 'px';
        canvasEl.width = W * ratio;
        canvasEl.height = H * ratio;
        const ctx = canvasEl.getContext('2d');
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    function setOilLevel(level) {
        targetOilLevel = Math.max(0, Math.min(1, level));
    }

    function resetOil() {
        oilLevel = 1;
        targetOilLevel = 1;
    }

    // ====================================================
    //  MAIN DRAW FUNCTION
    // ====================================================
    function drawDiya(ctx, oil, time, isBreak) {
        ctx.clearRect(0, 0, W, H);

        // Smooth oil interpolation
        oilLevel += (targetOilLevel - oilLevel) * 0.015;

        const cx = W / 2;
        const baseY = H * 0.62;

        // ---- Timer ring (rangoli arc) ----
        drawTimerRing(ctx, cx, baseY, time);

        // ---- Ambient light from flame ----
        drawAmbientGlow(ctx, cx, baseY, time);

        // ---- Ground shadow (under the diya) ----
        drawGroundShadow(ctx, cx, baseY);

        // ---- Diya body (3D bowl) ----
        drawDiyaBody(ctx, cx, baseY, time);

        // ---- Oil inside bowl ----
        drawOil(ctx, cx, baseY);

        // ---- Spout / Wick holder ----
        drawSpout(ctx, cx, baseY);

        // ---- Wick ----
        drawWick(ctx, cx, baseY);

        // ---- Flame ----
        if (oilLevel > 0.02) {
            drawFlame(ctx, cx, baseY, time);
        }

        // ---- Decorative engravings ----
        drawEngravings(ctx, cx, baseY);

        // ---- Break mode: Shilpkar refilling ----
        if (isBreak) {
            drawRefillCharacter(ctx, cx, baseY, time);
        }
    }

    // ---- RANGOLI TIMER RING ----
    function drawTimerRing(ctx, cx, baseY, time) {
        const ringCx = cx + 20; // Centered on diya + spout
        const ringCy = baseY - 10;
        const radius = 170;
        const beadCount = 108; // Sacred mala number
        const activeBeads = Math.round(beadCount * oilLevel);

        ctx.save();

        // === Outer ornamental track (thin dim ring) ===
        ctx.strokeStyle = 'rgba(201, 168, 76, 0.08)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(ringCx, ringCy, radius + 12, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(ringCx, ringCy, radius - 12, 0, Math.PI * 2);
        ctx.stroke();

        // === Background track (full dim circle) ===
        ctx.strokeStyle = 'rgba(201, 168, 76, 0.06)';
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.arc(ringCx, ringCy, radius, 0, Math.PI * 2);
        ctx.stroke();

        // === Active arc (sweeps from top, clockwise) ===
        const startAngle = -Math.PI / 2; // 12 o'clock
        const endAngle = startAngle + (Math.PI * 2 * oilLevel);

        if (oilLevel > 0.005) {
            // Glowing active arc
            const arcGrad = ctx.createLinearGradient(
                ringCx - radius, ringCy - radius,
                ringCx + radius, ringCy + radius
            );
            arcGrad.addColorStop(0, '#f0d060');
            arcGrad.addColorStop(0.3, '#e8b840');
            arcGrad.addColorStop(0.7, '#c99830');
            arcGrad.addColorStop(1, '#f0d060');

            // Outer glow of the arc
            ctx.strokeStyle = `rgba(232, 200, 80, ${0.15 + Math.sin(time * 2) * 0.05})`;
            ctx.lineWidth = 18;
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.arc(ringCx, ringCy, radius, startAngle, endAngle);
            ctx.stroke();

            // Main arc stroke
            ctx.strokeStyle = arcGrad;
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.arc(ringCx, ringCy, radius, startAngle, endAngle);
            ctx.stroke();
            ctx.lineCap = 'butt';

            // Bright tip at the leading edge
            const tipX = ringCx + Math.cos(endAngle) * radius;
            const tipY = ringCy + Math.sin(endAngle) * radius;
            const tipGlow = ctx.createRadialGradient(tipX, tipY, 0, tipX, tipY, 14);
            tipGlow.addColorStop(0, 'rgba(255, 240, 150, 0.6)');
            tipGlow.addColorStop(0.5, 'rgba(232, 200, 80, 0.2)');
            tipGlow.addColorStop(1, 'transparent');
            ctx.fillStyle = tipGlow;
            ctx.fillRect(tipX - 15, tipY - 15, 30, 30);
        }

        // === Mala beads (108 dots around the ring) ===
        for (let i = 0; i < beadCount; i++) {
            const angle = startAngle + (i / beadCount) * Math.PI * 2;
            const bx = ringCx + Math.cos(angle) * radius;
            const by = ringCy + Math.sin(angle) * radius;
            const isActive = i < activeBeads;

            // Every 27th bead is a marker (quarter points of the mala)
            const isMarker = i % 27 === 0;
            const beadSize = isMarker ? 4 : 1.8;

            if (isActive) {
                // Subtle pulse for the last few active beads
                const isNearTip = i >= activeBeads - 5;
                const pulse = isNearTip ? 0.7 + Math.sin(time * 4 + i) * 0.3 : 0.5;
                ctx.fillStyle = isMarker
                    ? `rgba(255, 220, 100, ${0.8 + Math.sin(time * 3) * 0.2})`
                    : `rgba(232, 200, 80, ${pulse})`;
            } else {
                ctx.fillStyle = isMarker
                    ? 'rgba(201, 168, 76, 0.12)'
                    : 'rgba(201, 168, 76, 0.04)';
            }

            ctx.beginPath();
            ctx.arc(bx, by, beadSize, 0, Math.PI * 2);
            ctx.fill();
        }

        // === Four cardinal ornaments (lotus petals at N/E/S/W) ===
        const cardinals = [
            -Math.PI / 2,          // Top
            0,                     // Right
            Math.PI / 2,           // Bottom
            Math.PI                // Left
        ];

        cardinals.forEach(angle => {
            const ox = ringCx + Math.cos(angle) * (radius + 12);
            const oy = ringCy + Math.sin(angle) * (radius + 12);
            const isLit = (angle - startAngle + Math.PI * 2) % (Math.PI * 2) <= (Math.PI * 2 * oilLevel) + 0.05;

            ctx.save();
            ctx.translate(ox, oy);
            ctx.rotate(angle + Math.PI / 2);

            // Small lotus/diamond shape
            ctx.fillStyle = isLit
                ? `rgba(232, 200, 80, ${0.7 + Math.sin(time * 2.5) * 0.2})`
                : 'rgba(201, 168, 76, 0.1)';

            ctx.beginPath();
            ctx.moveTo(0, -8);
            ctx.bezierCurveTo(5, -3, 5, 3, 0, 8);
            ctx.bezierCurveTo(-5, 3, -5, -3, 0, -8);
            ctx.fill();

            // Inner dot
            if (isLit) {
                ctx.fillStyle = 'rgba(255, 250, 200, 0.6)';
                ctx.beginPath();
                ctx.arc(0, 0, 2, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.restore();
        });

        ctx.restore();
    }

    // ---- AMBIENT GLOW ----
    function drawAmbientGlow(ctx, cx, baseY, time) {
        const glowPulse = 0.85 + Math.sin(time * 3) * 0.15;
        const spoutX = cx + 65;
        const glowY = baseY - 60;
        const radius = (120 + oilLevel * 80) * glowPulse;

        const glow = ctx.createRadialGradient(spoutX, glowY, 3, spoutX, glowY, radius);
        glow.addColorStop(0, `rgba(255, 180, 50, ${0.18 * oilLevel})`);
        glow.addColorStop(0.3, `rgba(255, 140, 30, ${0.08 * oilLevel})`);
        glow.addColorStop(0.7, `rgba(200, 100, 20, ${0.03 * oilLevel})`);
        glow.addColorStop(1, 'transparent');
        ctx.fillStyle = glow;
        ctx.fillRect(0, 0, W, H);

        // Warm wash on the ground
        const groundGlow = ctx.createRadialGradient(cx, baseY + 40, 10, cx, baseY + 40, 200);
        groundGlow.addColorStop(0, `rgba(255, 160, 40, ${0.06 * oilLevel})`);
        groundGlow.addColorStop(1, 'transparent');
        ctx.fillStyle = groundGlow;
        ctx.fillRect(0, baseY - 20, W, H - baseY + 20);
    }

    // ---- GROUND SHADOW ----
    function drawGroundShadow(ctx, cx, baseY) {
        ctx.save();
        // Main shadow ellipse
        const shadowGrad = ctx.createRadialGradient(cx, baseY + 38, 5, cx, baseY + 38, 100);
        shadowGrad.addColorStop(0, 'rgba(0, 0, 0, 0.4)');
        shadowGrad.addColorStop(0.5, 'rgba(0, 0, 0, 0.15)');
        shadowGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = shadowGrad;
        ctx.beginPath();
        ctx.ellipse(cx, baseY + 38, 100, 16, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // ---- DIYA BODY (3D Bowl) ----
    function drawDiyaBody(ctx, cx, baseY) {
        ctx.save();

        // === Bottom of the bowl (darker underside for 3D depth) ===
        const underGrad = ctx.createLinearGradient(cx - 70, baseY + 10, cx + 70, baseY + 30);
        underGrad.addColorStop(0, '#6b4420');
        underGrad.addColorStop(0.5, '#5a3818');
        underGrad.addColorStop(1, '#4a2e14');
        ctx.fillStyle = underGrad;
        ctx.beginPath();
        ctx.ellipse(cx, baseY + 22, 72, 14, 0, 0, Math.PI * 2);
        ctx.fill();

        // === Main bowl body (rich copper/terracotta with 3D gradient) ===
        const bodyGrad = ctx.createRadialGradient(cx - 20, baseY - 10, 5, cx + 10, baseY + 5, 90);
        bodyGrad.addColorStop(0, '#e8b860');   // Highlight (light hitting from left-top)
        bodyGrad.addColorStop(0.2, '#d4a048');  // Bright copper
        bodyGrad.addColorStop(0.5, '#c08a38');  // Mid copper
        bodyGrad.addColorStop(0.75, '#a06e28'); // Dark side
        bodyGrad.addColorStop(1, '#7a5020');    // Deep shadow edge

        ctx.fillStyle = bodyGrad;
        ctx.beginPath();
        ctx.moveTo(cx - 68, baseY + 5);
        // Left curve
        ctx.bezierCurveTo(cx - 75, baseY + 22, cx - 45, baseY + 32, cx, baseY + 30);
        // Right curve
        ctx.bezierCurveTo(cx + 45, baseY + 32, cx + 75, baseY + 22, cx + 68, baseY + 5);
        // Rim right
        ctx.bezierCurveTo(cx + 60, baseY - 12, cx + 48, baseY - 28, cx + 35, baseY - 30);
        // Top
        ctx.lineTo(cx - 35, baseY - 30);
        // Rim left
        ctx.bezierCurveTo(cx - 48, baseY - 28, cx - 60, baseY - 12, cx - 68, baseY + 5);
        ctx.closePath();
        ctx.fill();

        // === Rim highlight (polished metal edge — top of the bowl) ===
        const rimGrad = ctx.createLinearGradient(cx - 70, baseY - 32, cx + 70, baseY - 25);
        rimGrad.addColorStop(0, '#f0d070');
        rimGrad.addColorStop(0.3, '#e8c458');
        rimGrad.addColorStop(0.5, '#fff0b0');  // Bright specular highlight
        rimGrad.addColorStop(0.7, '#e8c458');
        rimGrad.addColorStop(1, '#c09838');

        ctx.strokeStyle = rimGrad;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(cx - 68, baseY + 5);
        ctx.bezierCurveTo(cx - 60, baseY - 12, cx - 48, baseY - 28, cx - 35, baseY - 30);
        ctx.lineTo(cx + 35, baseY - 30);
        ctx.bezierCurveTo(cx + 48, baseY - 28, cx + 60, baseY - 12, cx + 68, baseY + 5);
        ctx.stroke();

        // === Inner lip shadow (dark line just inside the rim for depth) ===
        ctx.strokeStyle = 'rgba(80, 50, 20, 0.5)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(cx - 60, baseY + 2);
        ctx.bezierCurveTo(cx - 52, baseY - 10, cx - 42, baseY - 24, cx - 30, baseY - 26);
        ctx.lineTo(cx + 30, baseY - 26);
        ctx.bezierCurveTo(cx + 42, baseY - 24, cx + 52, baseY - 10, cx + 60, baseY + 2);
        ctx.stroke();

        // === Specular highlight streak (3D shine on the bowl surface) ===
        ctx.save();
        ctx.globalAlpha = 0.25;
        const specGrad = ctx.createLinearGradient(cx - 50, baseY - 15, cx - 25, baseY + 15);
        specGrad.addColorStop(0, 'transparent');
        specGrad.addColorStop(0.4, 'rgba(255, 240, 180, 0.6)');
        specGrad.addColorStop(0.6, 'rgba(255, 240, 180, 0.6)');
        specGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = specGrad;
        ctx.beginPath();
        ctx.ellipse(cx - 30, baseY, 12, 28, -0.3, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // === Base/pedestal (small foot under the bowl) ===
        const baseGrad = ctx.createLinearGradient(cx - 25, baseY + 28, cx + 25, baseY + 40);
        baseGrad.addColorStop(0, '#c09838');
        baseGrad.addColorStop(0.5, '#a07828');
        baseGrad.addColorStop(1, '#7a5a1e');
        ctx.fillStyle = baseGrad;
        ctx.beginPath();
        ctx.ellipse(cx, baseY + 32, 30, 6, 0, 0, Math.PI * 2);
        ctx.fill();

        // Pedestal highlight
        ctx.strokeStyle = 'rgba(240, 210, 120, 0.4)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.ellipse(cx, baseY + 31, 30, 5, 0, Math.PI, 0); // Top half only
        ctx.stroke();

        ctx.restore();
    }

    // ---- OIL INSIDE BOWL ----
    function drawOil(ctx, cx, baseY) {
        if (oilLevel < 0.01) return;

        const maxOilDepth = 28; // How far oil can fill
        const currentDepth = maxOilDepth * oilLevel;
        const oilSurfaceY = baseY - 2 - currentDepth;
        const oilWidth = 28 * oilLevel + 10;

        ctx.save();

        // Oil body (dark liquid)
        const oilBodyGrad = ctx.createLinearGradient(0, oilSurfaceY, 0, baseY + 5);
        oilBodyGrad.addColorStop(0, `rgba(185, 130, 35, ${0.8 * oilLevel + 0.2})`);
        oilBodyGrad.addColorStop(0.6, `rgba(155, 100, 25, ${0.6 * oilLevel + 0.2})`);
        oilBodyGrad.addColorStop(1, `rgba(120, 75, 18, ${0.4 * oilLevel + 0.1})`);
        ctx.fillStyle = oilBodyGrad;
        ctx.beginPath();
        ctx.ellipse(cx, oilSurfaceY + 3, oilWidth, 6 * oilLevel + 2, 0, 0, Math.PI * 2);
        ctx.fill();

        // Oil surface reflection (shiny liquid surface)
        const reflGrad = ctx.createRadialGradient(cx - 8, oilSurfaceY + 1, 2, cx, oilSurfaceY + 2, oilWidth * 0.7);
        reflGrad.addColorStop(0, `rgba(255, 230, 140, ${0.35 * oilLevel})`);
        reflGrad.addColorStop(0.5, `rgba(220, 180, 80, ${0.15 * oilLevel})`);
        reflGrad.addColorStop(1, 'transparent');
        ctx.fillStyle = reflGrad;
        ctx.beginPath();
        ctx.ellipse(cx, oilSurfaceY + 2, oilWidth * 0.8, 4 * oilLevel + 1, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }

    // ---- SPOUT (wick holder extension) ----
    function drawSpout(ctx, cx, baseY) {
        ctx.save();

        const spoutStartX = cx + 35;
        const spoutEndX = cx + 80;
        const spoutY = baseY - 30;

        // Spout body (3D with gradient)
        const spoutGrad = ctx.createLinearGradient(spoutStartX, spoutY - 10, spoutEndX, spoutY + 5);
        spoutGrad.addColorStop(0, '#c89838');
        spoutGrad.addColorStop(0.4, '#b08030');
        spoutGrad.addColorStop(1, '#8a6020');
        ctx.fillStyle = spoutGrad;

        ctx.beginPath();
        ctx.moveTo(spoutStartX, spoutY);
        ctx.lineTo(spoutEndX, spoutY - 8);
        ctx.quadraticCurveTo(spoutEndX + 8, spoutY - 4, spoutEndX + 4, spoutY + 2);
        ctx.lineTo(spoutStartX, spoutY + 12);
        ctx.closePath();
        ctx.fill();

        // Spout top highlight
        ctx.strokeStyle = '#f0d870';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(spoutStartX, spoutY);
        ctx.lineTo(spoutEndX, spoutY - 8);
        ctx.quadraticCurveTo(spoutEndX + 8, spoutY - 4, spoutEndX + 4, spoutY + 2);
        ctx.stroke();

        // Spout underside shadow
        ctx.strokeStyle = 'rgba(60, 35, 10, 0.4)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(spoutStartX, spoutY + 12);
        ctx.lineTo(spoutEndX + 4, spoutY + 2);
        ctx.stroke();

        ctx.restore();
    }

    // ---- WICK ----
    function drawWick(ctx, cx, baseY) {
        const wickX = cx + 68;
        const wickBaseY = baseY - 34;

        // Wick shadow
        ctx.strokeStyle = 'rgba(0,0,0,0.3)';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(wickX + 1, wickBaseY + 1);
        ctx.lineTo(wickX + 1, wickBaseY - 13);
        ctx.stroke();

        // Wick body
        const wickGrad = ctx.createLinearGradient(0, wickBaseY, 0, wickBaseY - 14);
        wickGrad.addColorStop(0, '#3a2a15');
        wickGrad.addColorStop(0.5, '#2a1a0a');
        wickGrad.addColorStop(1, '#1a0e05');
        ctx.strokeStyle = wickGrad;
        ctx.lineWidth = 2.5;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(wickX, wickBaseY);
        ctx.lineTo(wickX, wickBaseY - 14);
        ctx.stroke();
        ctx.lineCap = 'butt';
    }

    // ---- FLAME (3D with inner/outer glow) ----
    function drawFlame(ctx, cx, baseY, time) {
        const wickX = cx + 68;
        const flameBaseY = baseY - 48;
        const flameFactor = 0.35 + oilLevel * 0.65;

        // Flame sway
        const sway = Math.sin(time * 4.2) * 2.5 + Math.sin(time * 7.1) * 1.2;
        const flameH = (42 + Math.sin(time * 5.5) * 4 + Math.sin(time * 8.3) * 2.5) * flameFactor;
        const flameW = (13 + Math.sin(time * 6.8) * 2) * flameFactor;

        ctx.save();

        // === Outer glow halo ===
        const haloRadius = (90 + Math.sin(time * 3.5) * 10) * flameFactor;
        const halo = ctx.createRadialGradient(wickX + sway * 0.3, flameBaseY - flameH * 0.35, 3, wickX, flameBaseY - flameH * 0.3, haloRadius);
        halo.addColorStop(0, `rgba(255, 200, 60, ${0.25 * oilLevel})`);
        halo.addColorStop(0.3, `rgba(255, 150, 30, ${0.1 * oilLevel})`);
        halo.addColorStop(0.6, `rgba(200, 100, 20, ${0.04 * oilLevel})`);
        halo.addColorStop(1, 'transparent');
        ctx.fillStyle = halo;
        ctx.fillRect(wickX - haloRadius, flameBaseY - flameH - haloRadius * 0.5, haloRadius * 2, haloRadius * 1.5 + flameH);

        // === Outer flame (orange-red) ===
        const outerGrad = ctx.createLinearGradient(0, flameBaseY, 0, flameBaseY - flameH);
        outerGrad.addColorStop(0, 'rgba(255, 100, 10, 0.92)');
        outerGrad.addColorStop(0.25, 'rgba(255, 140, 20, 0.85)');
        outerGrad.addColorStop(0.55, 'rgba(255, 190, 50, 0.6)');
        outerGrad.addColorStop(0.8, 'rgba(255, 220, 80, 0.25)');
        outerGrad.addColorStop(1, 'rgba(255, 240, 120, 0)');
        ctx.fillStyle = outerGrad;

        ctx.beginPath();
        ctx.moveTo(wickX, flameBaseY);
        ctx.bezierCurveTo(
            wickX - flameW * 1.2, flameBaseY - flameH * 0.2,
            wickX - flameW * 0.9 + sway * 0.5, flameBaseY - flameH * 0.65,
            wickX + sway, flameBaseY - flameH
        );
        ctx.bezierCurveTo(
            wickX + flameW * 0.9 + sway * 0.5, flameBaseY - flameH * 0.65,
            wickX + flameW * 1.2, flameBaseY - flameH * 0.2,
            wickX, flameBaseY
        );
        ctx.fill();

        // === Mid flame (golden) ===
        const midH = flameH * 0.7;
        const midW = flameW * 0.65;
        const midGrad = ctx.createLinearGradient(0, flameBaseY, 0, flameBaseY - midH);
        midGrad.addColorStop(0, 'rgba(255, 200, 50, 0.95)');
        midGrad.addColorStop(0.4, 'rgba(255, 230, 100, 0.8)');
        midGrad.addColorStop(0.8, 'rgba(255, 250, 180, 0.4)');
        midGrad.addColorStop(1, 'rgba(255, 255, 220, 0)');
        ctx.fillStyle = midGrad;

        ctx.beginPath();
        ctx.moveTo(wickX, flameBaseY);
        ctx.bezierCurveTo(
            wickX - midW, flameBaseY - midH * 0.25,
            wickX - midW * 0.7 + sway * 0.3, flameBaseY - midH * 0.7,
            wickX + sway * 0.6, flameBaseY - midH
        );
        ctx.bezierCurveTo(
            wickX + midW * 0.7 + sway * 0.3, flameBaseY - midH * 0.7,
            wickX + midW, flameBaseY - midH * 0.25,
            wickX, flameBaseY
        );
        ctx.fill();

        // === Inner flame core (white-hot) ===
        const innerH = flameH * 0.38;
        const innerW = flameW * 0.32;
        const innerGrad = ctx.createLinearGradient(0, flameBaseY, 0, flameBaseY - innerH);
        innerGrad.addColorStop(0, 'rgba(255, 255, 240, 0.98)');
        innerGrad.addColorStop(0.5, 'rgba(255, 255, 200, 0.7)');
        innerGrad.addColorStop(1, 'rgba(255, 240, 160, 0)');
        ctx.fillStyle = innerGrad;

        ctx.beginPath();
        ctx.moveTo(wickX, flameBaseY);
        ctx.bezierCurveTo(
            wickX - innerW, flameBaseY - innerH * 0.3,
            wickX - innerW * 0.5 + sway * 0.15, flameBaseY - innerH * 0.7,
            wickX + sway * 0.3, flameBaseY - innerH
        );
        ctx.bezierCurveTo(
            wickX + innerW * 0.5 + sway * 0.15, flameBaseY - innerH * 0.7,
            wickX + innerW, flameBaseY - innerH * 0.3,
            wickX, flameBaseY
        );
        ctx.fill();

        ctx.restore();
    }

    // ---- DECORATIVE ENGRAVINGS ----
    function drawEngravings(ctx, cx, baseY) {
        ctx.save();
        ctx.globalAlpha = 0.5;

        // Row of dots on the bowl
        ctx.fillStyle = '#f0d060';
        for (let i = -4; i <= 4; i++) {
            const dotX = cx + i * 12;
            const dotY = baseY + 12;
            ctx.beginPath();
            ctx.arc(dotX, dotY, 2, 0, Math.PI * 2);
            ctx.fill();
        }

        // Small diamond pattern below dots
        ctx.strokeStyle = '#e8c050';
        ctx.lineWidth = 0.8;
        for (let i = -3; i <= 3; i++) {
            const dx = cx + i * 14;
            const dy = baseY + 22;
            ctx.beginPath();
            ctx.moveTo(dx, dy - 3);
            ctx.lineTo(dx + 3, dy);
            ctx.lineTo(dx, dy + 3);
            ctx.lineTo(dx - 3, dy);
            ctx.closePath();
            ctx.stroke();
        }

        ctx.restore();
    }

    // ---- BREAK MODE: SHILPKAR REFILLING OIL ----
    function drawRefillCharacter(ctx, cx, baseY, time) {
        const charX = cx - 95;
        const charY = baseY - 5;
        const bobY = Math.sin(time * 2) * 3;

        ctx.save();

        // === Body (torso) ===
        const bodyGrad = ctx.createLinearGradient(charX - 15, charY - 40, charX + 15, charY);
        bodyGrad.addColorStop(0, '#c9903a');
        bodyGrad.addColorStop(1, '#a07030');
        ctx.fillStyle = bodyGrad;
        ctx.beginPath();
        ctx.ellipse(charX, charY + bobY - 18, 16, 24, 0, 0, Math.PI * 2);
        ctx.fill();

        // Dhoti/cloth wrap
        ctx.fillStyle = '#e8d8c0';
        ctx.beginPath();
        ctx.ellipse(charX, charY + bobY + 2, 18, 12, 0, 0, Math.PI);
        ctx.fill();

        // === Head ===
        const headGrad = ctx.createRadialGradient(charX - 3, charY + bobY - 49, 2, charX, charY + bobY - 46, 14);
        headGrad.addColorStop(0, '#e0b060');
        headGrad.addColorStop(1, '#c89040');
        ctx.fillStyle = headGrad;
        ctx.beginPath();
        ctx.arc(charX, charY + bobY - 46, 13, 0, Math.PI * 2);
        ctx.fill();

        // === Turban ===
        const turbanGrad = ctx.createLinearGradient(charX - 14, charY + bobY - 60, charX + 14, charY + bobY - 50);
        turbanGrad.addColorStop(0, '#d04a30');
        turbanGrad.addColorStop(0.5, '#b83a25');
        turbanGrad.addColorStop(1, '#a03020');
        ctx.fillStyle = turbanGrad;
        ctx.beginPath();
        ctx.ellipse(charX, charY + bobY - 55, 15, 8, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(charX, charY + bobY - 52, 13, Math.PI, 0);
        ctx.fill();

        // Turban jewel
        ctx.fillStyle = '#f0d060';
        ctx.beginPath();
        ctx.arc(charX, charY + bobY - 56, 3, 0, Math.PI * 2);
        ctx.fill();

        // === Arm holding oil pot ===
        ctx.strokeStyle = '#d0a050';
        ctx.lineWidth = 4;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(charX + 14, charY + bobY - 24);
        const armEndX = charX + 70 + Math.sin(time * 1.5) * 4;
        const armEndY = charY + bobY - 38 + Math.cos(time * 1.5) * 3;
        ctx.quadraticCurveTo(charX + 45, charY + bobY - 45, armEndX, armEndY);
        ctx.stroke();
        ctx.lineCap = 'butt';

        // === Oil pot ===
        const potGrad = ctx.createRadialGradient(armEndX + 3, armEndY - 2, 2, armEndX + 5, armEndY, 12);
        potGrad.addColorStop(0, '#a07040');
        potGrad.addColorStop(1, '#6a4828');
        ctx.fillStyle = potGrad;
        ctx.beginPath();
        ctx.ellipse(armEndX + 5, armEndY, 10, 8, -0.3, 0, Math.PI * 2);
        ctx.fill();

        // Pot rim
        ctx.strokeStyle = '#c09050';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.ellipse(armEndX + 5, armEndY - 3, 8, 3, -0.3, 0, Math.PI * 2);
        ctx.stroke();

        // === Oil stream (pouring arc) ===
        if (oilLevel < 0.98) {
            ctx.strokeStyle = `rgba(185, 130, 35, ${0.5 + Math.sin(time * 4) * 0.2})`;
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.moveTo(armEndX + 14, armEndY);
            ctx.bezierCurveTo(
                armEndX + 30, armEndY + 10 + Math.sin(time * 3) * 3,
                cx - 10, baseY - 35,
                cx, baseY - 28
            );
            ctx.stroke();

            // Drip splash on oil surface
            ctx.fillStyle = `rgba(200, 160, 50, ${0.3 + Math.sin(time * 5) * 0.15})`;
            ctx.beginPath();
            ctx.arc(cx, baseY - 26, 3 + Math.sin(time * 6) * 1, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.restore();
    }

    // ====================================================
    //  ANIMATION LOOP
    // ====================================================
    function startAnimation(mode) {
        running = true;
        flameTime = 0;
        const isBreak = mode === 'break';
        const ctx = isBreak ? breakCtx : focusCtx;

        function loop() {
            if (!running) return;
            flameTime += 0.016;
            drawDiya(ctx, oilLevel, flameTime, isBreak);
            animFrame = requestAnimationFrame(loop);
        }
        loop();
    }

    function stopAnimation() {
        running = false;
        if (animFrame) {
            cancelAnimationFrame(animFrame);
            animFrame = null;
        }
    }

    return {
        initFocus,
        initBreak,
        setOilLevel,
        startAnimation,
        stopAnimation,
        resetOil
    };
})();
