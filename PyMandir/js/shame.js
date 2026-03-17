/* ================================================
   Shame Module
   Wall of Shame messages and rendering
   ================================================ */

const Shame = (() => {
    const messages = [
        "The Shilpkar abandoned his post. The monkeys have taken over the construction site. 🐒",
        "Even the temple pigeons are more consistent than you. 🕊️",
        "The ancestors are NOT pleased. Two suns passed without a stone laid.",
        "Your temple weeps. The cracks grow deeper with your absence.",
        "The village children built a sandcastle more impressive than your commitment.",
        "Legend says a great builder once lived here. They took a 'short break.'",
        "The diya burned out. Nobody refilled the oil. How symbolic.",
        "A spider has built a better structure in the corner of your unfinished temple.",
        "The other Shilpkars are talking about you. And not kindly. 😤",
        "Two days without work. The stones have started to doubt your existence.",
        "Even Lord Vishwakarma, the divine architect, is shaking his head.",
        "The foundation is crying. Literally. Water seepage from neglect.",
        "Your tools are rusting. They miss you. Actually, they've given up on you.",
        "A passing traveler asked 'What ruins are these?' — It's your unfinished temple. 💀",
        "The temple bell rings, but not for celebration. It rings in disappointment.",
        "कर्म किये जा, फल की चिंता मत कर — but you're not even doing the कर्म!",
        "Two days missed. The stone mason guild is considering revoking your membership.",
        "The incense burned out. The prayers stopped. The builder vanished.",
        "A cow sat on your construction site. She's more productive than you. 🐄",
        "The stars aligned for your learning... and you were asleep.",
        "Your temple is now a tourist attraction: 'Ancient Ruins of Unfulfilled Potential.'",
        "Even Hanuman, who carried a mountain, couldn't carry your laziness.",
    ];

    function getMessages() {
        return messages;
    }

    function render(container, entries) {
        const emptyEl = document.getElementById('shame-empty');

        if (!entries || entries.length === 0) {
            if (emptyEl) emptyEl.style.display = '';
            return;
        }

        if (emptyEl) emptyEl.style.display = 'none';

        // Clear old entries (but keep the empty message element)
        const existingEntries = container.querySelectorAll('.shame-entry');
        existingEntries.forEach(e => e.remove());

        entries.forEach((entry, i) => {
            const el = document.createElement('div');
            el.className = 'shame-entry';
            el.style.animationDelay = `${i * 0.1}s`;
            el.innerHTML = `
                <span class="shame-icon">😤</span>
                <div class="shame-content">
                    <div class="shame-date">${formatDate(entry.date)} — Skipped ${entry.daysSkipped} days</div>
                    <div class="shame-message">"${entry.message}"</div>
                </div>
            `;
            container.appendChild(el);
        });
    }

    function formatDate(dateStr) {
        const d = new Date(dateStr + 'T00:00:00');
        return d.toLocaleDateString('en-IN', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    }

    return { getMessages, render };
})();
