/* ================================================
   Timer Module
   Focus timer logic with presets, custom, sessions
   ================================================ */

const Timer = (() => {
    let focusDuration = 25; // minutes
    let breakDuration = 5;
    let totalSessions = 4;
    let currentSession = 1;
    let timeRemaining = 0; // seconds
    let timerInterval = null;
    let mode = 'idle'; // 'idle' | 'focus' | 'break' | 'complete'
    let totalFocusThisRound = 0;

    function init() {
        // Preset buttons
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const focus = btn.dataset.focus;
                const brk = btn.dataset.break;

                const customSettings = document.getElementById('custom-timer-settings');
                if (focus === 'custom') {
                    customSettings.classList.add('visible');
                    updateFromCustomSliders();
                } else {
                    customSettings.classList.remove('visible');
                    focusDuration = parseInt(focus);
                    breakDuration = parseInt(brk);
                }
            });
        });

        // Custom sliders
        const focusSlider = document.getElementById('custom-focus');
        const breakSlider = document.getElementById('custom-break');
        const focusVal = document.getElementById('custom-focus-value');
        const breakVal = document.getElementById('custom-break-value');

        focusSlider.addEventListener('input', () => {
            focusVal.textContent = focusSlider.value;
            focusDuration = parseInt(focusSlider.value);
        });

        breakSlider.addEventListener('input', () => {
            breakVal.textContent = breakSlider.value;
            breakDuration = parseInt(breakSlider.value);
        });

        // Session pills
        document.querySelectorAll('.session-pill').forEach(pill => {
            pill.addEventListener('click', () => {
                document.querySelectorAll('.session-pill').forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                totalSessions = parseInt(pill.dataset.sessions);
            });
        });

        // Begin button
        document.getElementById('btn-begin-session').addEventListener('click', startFocus);

        // Cancel button
        document.getElementById('btn-cancel-session').addEventListener('click', cancelSession);

        // Skip break
        document.getElementById('btn-skip-break').addEventListener('click', skipBreak);

        // Back to dashboard
        document.getElementById('btn-back-dashboard').addEventListener('click', () => {
            hideAllTimerScreens();
            document.getElementById('timer-setup').classList.remove('hidden');
            document.getElementById('timer-setup').style.display = '';
            // Switch to dashboard tab
            document.querySelector('[data-tab="dashboard"]').click();
        });

        // Volume slider (Om chant)
        const volumeSlider = document.getElementById('volume-slider');
        const volumeIcon = document.getElementById('volume-icon');
        let isMuted = false;
        let lastVolume = 15;

        volumeSlider.addEventListener('input', () => {
            const val = parseInt(volumeSlider.value);
            Audio.setVolume(val / 100);
            isMuted = val === 0;
            updateVolumeIcon(val);
        });

        volumeIcon.addEventListener('click', () => {
            isMuted = !isMuted;
            if (isMuted) {
                lastVolume = parseInt(volumeSlider.value);
                volumeSlider.value = 0;
                Audio.setVolume(0);
                updateVolumeIcon(0);
            } else {
                volumeSlider.value = lastVolume || 15;
                Audio.setVolume(lastVolume / 100);
                updateVolumeIcon(lastVolume);
            }
        });

        function updateVolumeIcon(val) {
            if (val === 0) volumeIcon.textContent = '🔇';
            else if (val < 40) volumeIcon.textContent = '🔉';
            else volumeIcon.textContent = '🔊';
        }
    }

    function updateFromCustomSliders() {
        focusDuration = parseInt(document.getElementById('custom-focus').value);
        breakDuration = parseInt(document.getElementById('custom-break').value);
    }

    function startFocus() {
        mode = 'focus';
        currentSession = 1;
        totalFocusThisRound = 0;
        beginFocusSession();
    }

    function beginFocusSession() {
        mode = 'focus';
        timeRemaining = focusDuration * 60;

        hideAllTimerScreens();
        document.getElementById('timer-focus').classList.remove('hidden');

        // Update session counter
        document.getElementById('focus-session-counter').textContent =
            `Session ${currentSession} of ${totalSessions}`;

        // Init diya
        Diya.initFocus(document.getElementById('diya-canvas'));
        Diya.resetOil();
        Diya.startAnimation('focus');

        // Start Om chant (only on first focus session of a round)
        if (currentSession === 1) {
            Audio.startOm();
        }

        // Spawn focus particles
        spawnFocusParticles();

        // Start countdown
        updateFocusDisplay();
        timerInterval = setInterval(() => {
            timeRemaining--;

            // Update oil level
            const elapsed = (focusDuration * 60) - timeRemaining;
            const progress = elapsed / (focusDuration * 60);
            Diya.setOilLevel(1 - progress);

            updateFocusDisplay();

            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                totalFocusThisRound += focusDuration;
                onFocusComplete();
            }
        }, 1000);
    }

    function onFocusComplete() {
        Diya.stopAnimation();
        clearFocusParticles();

        // Play temple bell chime
        playTempleBell();

        if (currentSession < totalSessions) {
            // Start break
            beginBreak();
        } else {
            // All sessions done
            onAllSessionsComplete();
        }
    }

    function beginBreak() {
        mode = 'break';
        timeRemaining = breakDuration * 60;

        hideAllTimerScreens();
        document.getElementById('timer-break').classList.remove('hidden');

        // Init break diya (refilling)
        Diya.initBreak(document.getElementById('break-canvas'));
        Diya.setOilLevel(0);
        Diya.startAnimation('break');

        updateBreakDisplay();
        timerInterval = setInterval(() => {
            timeRemaining--;

            // Oil refills during break
            const elapsed = (breakDuration * 60) - timeRemaining;
            const progress = elapsed / (breakDuration * 60);
            Diya.setOilLevel(progress);

            updateBreakDisplay();

            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                Diya.stopAnimation();
                currentSession++;
                beginFocusSession();
            }
        }, 1000);
    }

    function skipBreak() {
        clearInterval(timerInterval);
        Diya.stopAnimation();
        currentSession++;
        beginFocusSession();
    }

    function onAllSessionsComplete() {
        mode = 'complete';
        hideAllTimerScreens();
        document.getElementById('timer-complete').classList.remove('hidden');

        // Stop Om chant
        Audio.stopOm();

        document.getElementById('complete-sessions').textContent = totalSessions;
        document.getElementById('complete-time').textContent = totalFocusThisRound + 'm';

        // Log session
        Storage.logSession(totalFocusThisRound, breakDuration * (totalSessions - 1), totalSessions);

        // Check achievements
        const data = Storage.load();
        const newAchievements = Achievements.checkAll(data);
        Storage.save(data);

        // Show toast for new achievements
        newAchievements.forEach((ach, i) => {
            setTimeout(() => {
                showToast(`🏆 Achievement Unlocked: ${ach.icon} ${ach.name}`);
            }, 1000 + i * 1500);
        });

        // Refresh dashboard when we return
        if (typeof Dashboard !== 'undefined') {
            Dashboard.refresh();
        }
    }

    function cancelSession() {
        clearInterval(timerInterval);
        Diya.stopAnimation();
        clearFocusParticles();
        Audio.stopOm();
        mode = 'idle';

        // Log partial session if at least 1 minute passed
        const elapsed = focusDuration - Math.ceil(timeRemaining / 60);
        if (elapsed >= 1) {
            totalFocusThisRound += elapsed;
            Storage.logSession(totalFocusThisRound, 0, currentSession);
            const data = Storage.load();
            Achievements.checkAll(data);
            Storage.save(data);
        }

        hideAllTimerScreens();
        document.getElementById('timer-setup').classList.remove('hidden');
        document.getElementById('timer-setup').style.display = '';
    }

    function hideAllTimerScreens() {
        ['timer-setup', 'timer-focus', 'timer-break', 'timer-complete'].forEach(id => {
            const el = document.getElementById(id);
            el.classList.add('hidden');
        });
    }

    function updateFocusDisplay() {
        const min = Math.floor(timeRemaining / 60);
        const sec = timeRemaining % 60;
        document.getElementById('focus-time').textContent =
            `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
    }

    function updateBreakDisplay() {
        const min = Math.floor(timeRemaining / 60);
        const sec = timeRemaining % 60;
        document.getElementById('break-time').textContent =
            `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
    }

    // Focus particles
    let focusParticleInterval;
    function spawnFocusParticles() {
        const container = document.getElementById('focus-particles');
        focusParticleInterval = setInterval(() => {
            const p = document.createElement('div');
            p.className = 'particle particle--ember';
            const size = Math.random() * 4 + 2;
            p.style.width = size + 'px';
            p.style.height = size + 'px';
            p.style.left = (Math.random() * 100) + '%';
            p.style.bottom = '-10px';
            p.style.setProperty('--drift', (Math.random() * 60 - 30) + 'px');
            p.style.animationDuration = (Math.random() * 6 + 5) + 's';
            container.appendChild(p);
            setTimeout(() => p.remove(), 11000);
        }, 400);
    }

    function clearFocusParticles() {
        if (focusParticleInterval) {
            clearInterval(focusParticleInterval);
            focusParticleInterval = null;
        }
        const container = document.getElementById('focus-particles');
        if (container) container.innerHTML = '';
    }

    return { init };
})();

// Toast helper
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('toast-exit');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Temple Bell Chime — synthesized metallic bell strike
function playTempleBell() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const now = ctx.currentTime;

        // Strike tone (fundamental)
        const osc1 = ctx.createOscillator();
        const gain1 = ctx.createGain();
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(830, now); // High bell tone
        gain1.gain.setValueAtTime(0.4, now);
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 3);
        osc1.connect(gain1);
        gain1.connect(ctx.destination);
        osc1.start(now);
        osc1.stop(now + 3);

        // Harmonic overtone
        const osc2 = ctx.createOscillator();
        const gain2 = ctx.createGain();
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(1660, now); // 2nd harmonic
        gain2.gain.setValueAtTime(0.15, now);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 2);
        osc2.connect(gain2);
        gain2.connect(ctx.destination);
        osc2.start(now);
        osc2.stop(now + 2);

        // Third overtone — shimmer
        const osc3 = ctx.createOscillator();
        const gain3 = ctx.createGain();
        osc3.type = 'sine';
        osc3.frequency.setValueAtTime(2490, now); // 3rd harmonic
        gain3.gain.setValueAtTime(0.06, now);
        gain3.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
        osc3.connect(gain3);
        gain3.connect(ctx.destination);
        osc3.start(now);
        osc3.stop(now + 1.5);

        // Second strike (slightly delayed for depth)
        const osc4 = ctx.createOscillator();
        const gain4 = ctx.createGain();
        osc4.type = 'sine';
        osc4.frequency.setValueAtTime(835, now + 0.8);
        gain4.gain.setValueAtTime(0, now);
        gain4.gain.setValueAtTime(0.25, now + 0.8);
        gain4.gain.exponentialRampToValueAtTime(0.001, now + 3.5);
        osc4.connect(gain4);
        gain4.connect(ctx.destination);
        osc4.start(now + 0.8);
        osc4.stop(now + 3.5);

        // Cleanup
        setTimeout(() => ctx.close(), 4000);
    } catch (e) {
        console.warn('Bell sound failed:', e);
    }
}
