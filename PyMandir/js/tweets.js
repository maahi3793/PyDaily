/* ================================================
   Tweets Module
   Tweet template generator
   ================================================ */

const Tweets = (() => {
    let selectedTemplate = 'summary';

    const templates = {
        summary: (day, topic, takeaway) =>
`Day ${day} of #PythonLearning 🐍

Today I explored ${topic} — and here's what clicked:

${takeaway}

Small wins compound. One stone at a time. 🏛️

#100DaysOfCode #Python #LearningInPublic`,

        tip: (day, topic, takeaway) =>
`🐍 Python Tip — Day ${day}

💡 Topic: ${topic}

${takeaway}

If you're also learning Python, save this for later! 🔖

#PythonTips #100DaysOfCode #CodingJourney`,

        milestone: (day, topic, takeaway) =>
`🎉 Day ${day} Milestone! 🐍

I've been consistently learning Python and today I covered ${topic}.

Key insight:
${takeaway}

The temple grows, one stone at a time. 🏛️🔥

#PythonLearning #100DaysOfCode #Consistency #LearningInPublic`
    };

    function init() {
        // Auto-fill day number
        const data = Storage.load();
        document.getElementById('tweet-day').value = data.totalDaysStudied || 1;

        // Template pills
        document.querySelectorAll('.template-pill').forEach(pill => {
            pill.addEventListener('click', () => {
                document.querySelectorAll('.template-pill').forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                selectedTemplate = pill.dataset.template;
            });
        });

        // Generate
        document.getElementById('btn-generate-tweet').addEventListener('click', generateTweet);

        // Copy
        document.getElementById('btn-copy-tweet').addEventListener('click', copyTweet);

        // Save
        document.getElementById('btn-save-tweet').addEventListener('click', saveTweet);

        renderHistory();
    }

    function generateTweet() {
        const day = document.getElementById('tweet-day').value || '?';
        const topic = document.getElementById('tweet-topic').value.trim() || 'Python concepts';
        const takeaway = document.getElementById('tweet-takeaway').value.trim() || 'Every day I learn something new.';

        const tweet = templates[selectedTemplate](day, topic, takeaway);

        document.getElementById('tweet-preview').textContent = tweet;
        document.getElementById('tweet-preview-container').classList.remove('hidden');
    }

    function copyTweet() {
        const text = document.getElementById('tweet-preview').textContent;
        navigator.clipboard.writeText(text).then(() => {
            showToast('📋 Tweet copied to clipboard!');
        }).catch(() => {
            // Fallback
            const ta = document.createElement('textarea');
            ta.value = text;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            showToast('📋 Tweet copied!');
        });
    }

    function saveTweet() {
        const text = document.getElementById('tweet-preview').textContent;
        if (!text) return;

        Storage.update(data => {
            data.tweets.unshift({
                id: Date.now(),
                text,
                template: selectedTemplate,
                createdAt: new Date().toISOString()
            });
        });

        // Check achievements
        const data = Storage.load();
        const newAch = Achievements.checkAll(data);
        Storage.save(data);
        newAch.forEach((ach, i) => {
            setTimeout(() => showToast(`🏆 ${ach.icon} ${ach.name} unlocked!`), i * 1500);
        });

        showToast('💾 Tweet saved!');
        renderHistory();
    }

    function renderHistory() {
        const data = Storage.load();
        const container = document.getElementById('tweet-history');

        if (data.tweets.length === 0) {
            container.innerHTML = '<h3 class="subsection-title">Saved Tweets</h3>' +
                '<p style="color: var(--text-dim); font-style: italic; padding: 20px 0;">No tweets saved yet. Generate your first one above!</p>';
            return;
        }

        const html = '<h3 class="subsection-title">Saved Tweets</h3>' +
            data.tweets.map(t => `
                <div class="tweet-history-item" data-id="${t.id}">
                    <div class="tweet-history-date">${formatDate(t.createdAt)}</div>
                    <div class="tweet-history-text">${escapeHtml(t.text)}</div>
                </div>
            `).join('');

        container.innerHTML = html;

        // Click to load into preview
        container.querySelectorAll('.tweet-history-item').forEach(item => {
            item.addEventListener('click', () => {
                const tweet = data.tweets.find(t => t.id === parseInt(item.dataset.id));
                if (tweet) {
                    document.getElementById('tweet-preview').textContent = tweet.text;
                    document.getElementById('tweet-preview-container').classList.remove('hidden');
                }
            });
        });
    }

    function formatDate(isoStr) {
        const d = new Date(isoStr);
        return d.toLocaleDateString('en-IN', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    return { init };
})();
