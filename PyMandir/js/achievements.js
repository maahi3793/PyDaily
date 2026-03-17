/* ================================================
   Achievements Module
   Definitions and unlock logic
   ================================================ */

const Achievements = (() => {
    const definitions = [
        {
            id: 'first_flame',
            icon: '🔥',
            name: 'First Flame',
            description: 'Complete your first focus session',
            check: data => data.totalSessions >= 1
        },
        {
            id: 'week_warrior',
            icon: '📅',
            name: 'Week Warrior',
            description: '7-day study streak',
            check: data => data.bestStreak >= 7
        },
        {
            id: 'monthly_master',
            icon: '🗓️',
            name: 'Monthly Master',
            description: '30-day study streak',
            check: data => data.bestStreak >= 30
        },
        {
            id: 'first_tweet',
            icon: '🐦',
            name: 'First Tweet',
            description: 'Generate your first tweet',
            check: data => data.tweets.length >= 1
        },
        {
            id: 'deep_thinker',
            icon: '⏱️',
            name: 'Deep Thinker',
            description: 'Complete a 50+ minute session',
            check: data => data.sessions.some(s => s.focusMinutes >= 50)
        },
        {
            id: 'century',
            icon: '🏅',
            name: 'Century',
            description: '100 total focus sessions',
            check: data => data.totalSessions >= 100
        },
        {
            id: 'stage_2',
            icon: '🧱',
            name: 'Walls Rising',
            description: 'Temple reaches Stage 2',
            check: data => data.templeStage >= 2
        },
        {
            id: 'stage_3',
            icon: '🚪',
            name: 'Carved Doorway',
            description: 'Temple reaches Stage 3',
            check: data => data.templeStage >= 3
        },
        {
            id: 'stage_4',
            icon: '🎨',
            name: 'Intricate Carvings',
            description: 'Temple reaches Stage 4',
            check: data => data.templeStage >= 4
        },
        {
            id: 'stage_5',
            icon: '🕌',
            name: 'Shikhara Rising',
            description: 'Temple reaches Stage 5',
            check: data => data.templeStage >= 5
        },
        {
            id: 'stage_6',
            icon: '🏛️',
            name: 'Grand Temple',
            description: 'Temple reaches its final form',
            check: data => data.templeStage >= 6
        },
        {
            id: 'note_taker',
            icon: '📝',
            name: 'Note Taker',
            description: 'Write 10 daily notes',
            check: data => data.notes.length >= 10
        },
        {
            id: 'topic_master',
            icon: '✅',
            name: 'Topic Master',
            description: 'Complete 10 planned topics',
            check: data => data.topics.filter(t => t.status === 'completed').length >= 10
        },
        {
            id: 'shame_survivor',
            icon: '😅',
            name: 'Shame Survivor',
            description: 'Come back after a shame entry',
            check: data => data.shameEntries.length > 0 && data.currentStreak >= 1
        }
    ];

    function checkAll(data) {
        const newlyUnlocked = [];
        for (const ach of definitions) {
            if (!data.unlockedAchievements.includes(ach.id) && ach.check(data)) {
                data.unlockedAchievements.push(ach.id);
                newlyUnlocked.push(ach);
            }
        }
        return newlyUnlocked;
    }

    function getAll() {
        return definitions;
    }

    return { checkAll, getAll };
})();
