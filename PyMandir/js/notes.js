/* ================================================
   Notes Module
   Simple daily notes
   ================================================ */

const Notes = (() => {
    function init() {
        document.getElementById('btn-save-notes').addEventListener('click', saveNotes);

        // Load today's notes if any
        const data = Storage.load();
        const today = Storage.getToday();
        const todayNote = data.notes.find(n => n.date === today);
        if (todayNote) {
            document.getElementById('notes-textarea').value = todayNote.text;
        }

        renderHistory();
    }

    function saveNotes() {
        const text = document.getElementById('notes-textarea').value.trim();
        if (!text) return;

        const today = Storage.getToday();

        Storage.update(data => {
            const existing = data.notes.find(n => n.date === today);
            if (existing) {
                existing.text = text;
            } else {
                data.notes.unshift({ date: today, text });
            }
        });

        // Check achievements
        const data = Storage.load();
        const newAch = Achievements.checkAll(data);
        Storage.save(data);
        newAch.forEach((ach, i) => {
            setTimeout(() => showToast(`🏆 ${ach.icon} ${ach.name} unlocked!`), i * 1500);
        });

        showToast('📝 Notes saved!');
        renderHistory();
    }

    function renderHistory() {
        const data = Storage.load();
        const container = document.getElementById('notes-history');
        const emptyEl = document.getElementById('notes-empty');

        if (data.notes.length === 0) {
            emptyEl.style.display = '';
            container.innerHTML = '<h3 class="subsection-title">Past Notes</h3>';
            return;
        }

        emptyEl.style.display = 'none';

        const html = '<h3 class="subsection-title">Past Notes</h3>' +
            data.notes.map(n => `
                <div class="note-entry">
                    <div class="note-date">${formatDate(n.date)}</div>
                    <div class="note-text">${escapeHtml(n.text)}</div>
                </div>
            `).join('');

        container.innerHTML = html;
    }

    function formatDate(dateStr) {
        const d = new Date(dateStr + 'T00:00:00');
        return d.toLocaleDateString('en-IN', {
            weekday: 'short',
            day: 'numeric',
            month: 'long',
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
