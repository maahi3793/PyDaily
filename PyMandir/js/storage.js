/* ================================================
   Storage Module
   LocalStorage abstraction for all app data
   ================================================ */

const Storage = (() => {
    const STORAGE_KEY = 'pymandir_data';

    const defaultData = () => ({
        // Streak & session tracking
        sessions: [],           // { date, focusMinutes, breakMinutes, count, timestamp }
        currentStreak: 0,
        bestStreak: 0,
        lastActiveDate: null,   // 'YYYY-MM-DD'

        // Topics
        topics: [],             // { id, name, status: 'not-started'|'in-progress'|'completed', createdAt }

        // Notes
        notes: [],              // { date, text }

        // Tweets
        tweets: [],             // { id, text, template, createdAt }

        // Wall of Shame
        shameEntries: [],       // { date, message, daysSkipped }

        // Achievements
        unlockedAchievements: [], // achievement IDs

        // Stats
        totalFocusMinutes: 0,
        totalSessions: 0,
        totalDaysStudied: 0,

        // Temple
        templeStage: 1,
        templeDaysInStage: 0,
        hasCracks: false,
    });

    function load() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return defaultData();
            const data = JSON.parse(raw);
            // Merge with defaults to handle schema changes
            return { ...defaultData(), ...data };
        } catch (e) {
            console.error('Storage load error:', e);
            return defaultData();
        }
    }

    function save(data) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch (e) {
            console.error('Storage save error:', e);
        }
    }

    function update(fn) {
        const data = load();
        fn(data);
        save(data);
        return data;
    }

    function getToday() {
        const d = new Date();
        return d.toISOString().split('T')[0]; // 'YYYY-MM-DD'
    }

    function daysBetween(dateStr1, dateStr2) {
        const d1 = new Date(dateStr1);
        const d2 = new Date(dateStr2);
        const diff = Math.abs(d2 - d1);
        return Math.floor(diff / (1000 * 60 * 60 * 24));
    }

    function checkAndUpdateStreak() {
        return update(data => {
            const today = getToday();
            if (!data.lastActiveDate) return;

            const gap = daysBetween(data.lastActiveDate, today);

            if (gap >= 2) {
                // Streak broken! Add shame if 2+ days skipped
                if (!data.shameEntries.find(e => e.date === today)) {
                    const shameMessages = Shame.getMessages();
                    const msg = shameMessages[Math.floor(Math.random() * shameMessages.length)];
                    data.shameEntries.unshift({
                        date: today,
                        message: msg,
                        daysSkipped: gap
                    });
                }
                data.currentStreak = 0;
                data.hasCracks = true;
            }
        });
    }

    function logSession(focusMinutes, breakMinutes, sessionCount) {
        return update(data => {
            const today = getToday();

            data.sessions.push({
                date: today,
                focusMinutes,
                breakMinutes,
                count: sessionCount,
                timestamp: Date.now()
            });

            data.totalFocusMinutes += focusMinutes;
            data.totalSessions += 1; // Count as 1 logged entry per call

            // Update streak
            const lastDate = data.lastActiveDate;
            if (!lastDate) {
                data.currentStreak = 1;
            } else {
                const gap = daysBetween(lastDate, today);
                if (gap === 0) {
                    // Same day, streak unchanged
                } else if (gap === 1) {
                    data.currentStreak += 1;
                } else {
                    data.currentStreak = 1; // reset
                }
            }

            if (data.currentStreak > data.bestStreak) {
                data.bestStreak = data.currentStreak;
            }

            // Count unique study days
            const uniqueDays = new Set(data.sessions.map(s => s.date));
            data.totalDaysStudied = uniqueDays.size;

            data.lastActiveDate = today;
            data.hasCracks = false;

            // Update temple stage
            updateTempleStage(data);
        });
    }

    function updateTempleStage(data) {
        const days = data.totalDaysStudied;
        if (days >= 90) { data.templeStage = 6; data.templeDaysInStage = days - 90; }
        else if (days >= 61) { data.templeStage = 5; data.templeDaysInStage = days - 61; }
        else if (days >= 36) { data.templeStage = 4; data.templeDaysInStage = days - 36; }
        else if (days >= 22) { data.templeStage = 3; data.templeDaysInStage = days - 22; }
        else if (days >= 8) { data.templeStage = 2; data.templeDaysInStage = days - 8; }
        else { data.templeStage = 1; data.templeDaysInStage = days; }
    }

    function getTodaySessions() {
        const data = load();
        const today = getToday();
        return data.sessions.filter(s => s.date === today);
    }

    return {
        load,
        save,
        update,
        getToday,
        daysBetween,
        checkAndUpdateStreak,
        logSession,
        getTodaySessions,
        clearAllData: () => { localStorage.removeItem(STORAGE_KEY); }
    };
})();
