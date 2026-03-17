/* ================================================
   App Module
   Navigation, initialization, ambient particles
   ================================================ */

const App = (() => {
    function init() {
        initNavigation();
        initParticles();

        // Initialize all modules
        Dashboard.init();
        Timer.init();
        Topics.init();
        Notes.init();
        Tweets.init();
        Stats.init();

        // Apply stagger animations to dashboard cards
        document.querySelectorAll('.dashboard-grid .card').forEach(card => {
            card.classList.add('stagger-in');
        });
    }

    function initNavigation() {
        const navBtns = document.querySelectorAll('.nav-btn');
        const tabs = document.querySelectorAll('.tab-content');

        navBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const target = btn.dataset.tab;

                // Update active nav button
                navBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Show target tab
                tabs.forEach(tab => tab.classList.remove('active'));
                const targetTab = document.getElementById('tab-' + target);
                if (targetTab) {
                    targetTab.classList.add('active');
                }

                // Refresh specific tabs when navigated to
                if (target === 'dashboard') Dashboard.refresh();
                if (target === 'stats') Stats.render();

                // Make sure timer setup is visible when navigating to timer tab
                if (target === 'timer') {
                    const setup = document.getElementById('timer-setup');
                    // Only show setup if no timer screen is active
                    const focusVisible = !document.getElementById('timer-focus').classList.contains('hidden');
                    const breakVisible = !document.getElementById('timer-break').classList.contains('hidden');
                    const completeVisible = !document.getElementById('timer-complete').classList.contains('hidden');
                    if (!focusVisible && !breakVisible && !completeVisible) {
                        setup.classList.remove('hidden');
                        setup.style.display = '';
                    }
                }
            });
        });
    }

    function initParticles() {
        const container = document.getElementById('particles-container');
        if (!container) return;

        // Spawn ambient particles periodically
        setInterval(() => {
            spawnAmbientParticle(container);
        }, 1200);

        // Initial batch
        for (let i = 0; i < 5; i++) {
            setTimeout(() => spawnAmbientParticle(container), i * 300);
        }
    }

    function spawnAmbientParticle(container) {
        const p = document.createElement('div');
        const isFirefly = Math.random() > 0.5;
        p.className = `particle ${isFirefly ? 'particle--firefly' : 'particle--ember'}`;

        const size = Math.random() * 3 + 1.5;
        p.style.width = size + 'px';
        p.style.height = size + 'px';
        p.style.left = (Math.random() * 100) + '%';
        p.style.bottom = '-5px';
        p.style.setProperty('--drift', (Math.random() * 80 - 40) + 'px');

        const duration = Math.random() * 10 + 8;
        p.style.animationDuration = duration + 's';

        container.appendChild(p);
        setTimeout(() => p.remove(), duration * 1000);
    }

    return { init };
})();

// Boot the app
document.addEventListener('DOMContentLoaded', App.init);
