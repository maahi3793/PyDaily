/* ================================================
   Stats Module
   Renders stats cards and achievements grid
   ================================================ */

const Stats = (() => {
    function init() {
        render();
    }

    function render() {
        const data = Storage.load();

        // Stat cards
        document.getElementById('stat-current-streak').textContent = data.currentStreak;
        document.getElementById('stat-best-streak').textContent = data.bestStreak;
        document.getElementById('stat-total-days').textContent = data.totalDaysStudied;
        document.getElementById('stat-total-sessions').textContent = data.totalSessions;
        document.getElementById('stat-shame-count').textContent = data.shameEntries.length;

        const hours = Math.floor(data.totalFocusMinutes / 60);
        const mins = data.totalFocusMinutes % 60;
        document.getElementById('stat-total-hours').textContent =
            hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;

        // Achievements grid
        renderAchievements(data);
    }

    function renderAchievements(data) {
        const grid = document.getElementById('achievements-grid');
        const all = Achievements.getAll();

        grid.innerHTML = all.map(ach => {
            const unlocked = data.unlockedAchievements.includes(ach.id);
            return `
                <div class="achievement-card ${unlocked ? 'unlocked' : 'locked'}">
                    <span class="achievement-icon">${ach.icon}</span>
                    <div class="achievement-name">${ach.name}</div>
                    <div class="achievement-desc">${ach.description}</div>
                </div>
            `;
        }).join('');
    }

    return { init, render };
})();
