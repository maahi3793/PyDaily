/* ================================================
   Dashboard Module
   Renders streak, temple, today stats, shame wall
   ================================================ */

const Dashboard = (() => {
    function init() {
        refresh();

        // Start focus button
        document.getElementById('btn-start-focus').addEventListener('click', () => {
            document.querySelector('[data-tab="timer"]').click();
        });
    }

    function refresh() {
        const data = Storage.load();

        // Check streak on load
        Storage.checkAndUpdateStreak();
        const freshData = Storage.load();

        // Streak numbers
        document.getElementById('streak-number').textContent = freshData.currentStreak;
        document.getElementById('sidebar-streak').textContent = freshData.currentStreak;
        document.getElementById('best-streak').textContent = freshData.bestStreak;
        document.getElementById('total-days').textContent = freshData.totalDaysStudied;

        // Temple
        Temple.init(document.getElementById('temple-canvas'));
        Temple.draw(freshData.templeStage, freshData.hasCracks);

        // Temple stage badge
        document.getElementById('temple-stage-badge').textContent = `Stage ${freshData.templeStage}`;

        // Temple progress
        const stageThresholds = [7, 14, 14, 25, 29, Infinity];
        const daysNeeded = stageThresholds[freshData.templeStage - 1];
        const pct = freshData.templeStage >= 6
            ? 100
            : Math.min(100, (freshData.templeDaysInStage / daysNeeded) * 100);
        document.getElementById('temple-progress-fill').style.width = pct + '%';
        document.getElementById('temple-progress-label').textContent =
            freshData.templeStage >= 6
                ? '🏛️ Temple Complete! You are a Grand Architect.'
                : `${freshData.templeDaysInStage} / ${daysNeeded} days to Stage ${freshData.templeStage + 1}`;

        // Today stats
        const todaySessions = Storage.getTodaySessions();
        const todaySessionCount = todaySessions.length; // Count of logged entries today
        const todayFocus = todaySessions.reduce((sum, s) => sum + s.focusMinutes, 0);
        document.getElementById('today-sessions').textContent = todaySessionCount;
        document.getElementById('today-focus-time').textContent = todayFocus > 0 ? todayFocus + 'm' : '0m';

        // Topics done today (count completed topics)
        const completedTopics = freshData.topics.filter(t => t.status === 'completed').length;
        document.getElementById('today-topics').textContent = completedTopics;

        // Shame wall
        Shame.render(document.getElementById('shame-wall'), freshData.shameEntries);
    }

    return { init, refresh };
})();
