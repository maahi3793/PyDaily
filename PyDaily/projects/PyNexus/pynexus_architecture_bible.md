# PyNexus: The Architecture Bible (v3.0)

> **Instructions for the New Builder:**
> This document is your Source of Truth. You are building **PyNexus**, a desktop application using **Flet** (Python) and **Supabase**.
> Follow these specifications exactly. You do not need to ask clarifying questions.

---

## 1. Project Overview
**PyNexus** is a high-fidelity desktop companion app for students within the **PyDaily Ecosystem**.
It serves two masters:
1.  **The Reader (Passive):** A Kindle-class reading experience for emails and textbooks.
2.  **The Forge (Active):** A Job Simulator that creates files on disk and creates "Tickets" for building a real product.

**Tech Stack:**
*   **Frontend:** Flet (`flet`) - Native Python UI.
*   **Backend:** Supabase (`supabase`) - Auth & Data.
*   **Local Ops:** `GitPython`, `subprocess`.

---

## 2. Directory Structure
Initialize the project exactly as follows:

```text
PyNexus/
├── assets/                  # Icons, images
├── src/
│   ├── components/
│   │   ├── sidebar.py
│   │   ├── reader_view.py   # The Kindle UI
│   │   └── ticket_board.py
│   ├── views/
│   │   ├── login.py
│   │   ├── dashboard.py
│   │   ├── library.py
│   │   └── build_lab.py
│   ├── services/
│   │   ├── auth.py
│   │   ├── content_manager.py # Merges Mails/Book/Battles
│   │   └── workspace.py     # File System Logic
│   ├── main.py
│   └── app_state.py
├── .env
├── requirements.txt
└── README.md
```

---

## 3. Data Sources & Schema (Supabase)

### 3.1 Content Aggregation (The Library)
PyNexus does not have its own content table. It aggregates three existing sources:
1.  **Daily Lessons:** From table `daily_mails` (Column: `clean_content`).
2.  **Deep Dives:** From table `textbook_chapters` (Columns: `content_part1_theory`, `content_part2_practice`).
3.  **Challenges:** From table `boss_battles` (Column: `mission_brief`).

**Builder Note:** You must create a `ContentService` that fetches from all three and presents them as a unified "Timeline" (Day 1 -> Day 180).

### 3.2 Practice Problems (The Forge)
Execute this SQL to enable the Exercise Engine:
```sql
CREATE TABLE IF NOT EXISTS exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    day_number INT NOT NULL,
    filename TEXT NOT NULL, -- e.g. "loop_practice.py"
    starter_code TEXT, -- The scaffolding
    solution_code TEXT,
    test_code TEXT -- Pytest code
);
```
*(Validation Fallback: If a lesson has no entry in `exercises`, the app should generate a placeholder file or use AI generation in future phases).*

---

## 4. Functional Requirements (The "Must Haves")

### 4.1 The "Kindle" Experience
*   **Aesthetics:** High typography standards are non-negotiable.
    *   **Font:** Serif for body text (e.g., *Merriweather* or *Georgia*), JetBrains Mono for code.
    *   **Themes:** Light, Dark, Sepia.
    *   **Focus Mode:** Sidebar collapses, reading area centers.
*   **Navigation:** "Day 1" is a container that holds the Email Lesson AND the Textbook Chapter. User swipes/clicks between them seamlessly.

### 4.2 The "Job Simulator" Workflow
*   **Context:** The user isn't doing "Homework"; they are "Working a Ticket".
*   **Action:**
    1.  User clicks **"Start Job"** on Day 4.
    2.  App creates `~/PyDaily/Day04_Loops/`.
    3.  App creates `main.py` (Starter Code) and `tests/test_main.py`.
    4.  App **Opens VS Code** to that folder immediately.
*   **Verification:**
    *   App watches the file system (or user clicks "Run Tests").
    *   App runs `subprocess.run(['pytest'])`.
    *   **Green Bar:** "Ticket Resolved. XP Awarded."

### 4.3 The Capstone (The Trading Terminal)
*   Visualized as a **Kanban Board**.
*   Tickets are Locked until specific Days are completed.
    *   *Day 10 (Requests Lib)* -> Unlocks Ticket: "Fetch Bitcoin Price".
    *   *Day 20 (Pandas)* -> Unlocks Ticket: "Calculate Moving Average".
*   This creates a "Meta-Game" where learning unlocks building.

---

## 5. Environment Variables
```ini
SUPABASE_URL="https://vaxkvxuougfeqzednyaa.supabase.co"
SUPABASE_KEY="[USER_MUST_PROVIDE_ANON_KEY]"
# Optional: OPENAI_KEY (For future AI generation)
```

## 6. Implementation Strategy (For New Agent)
1.  **Setup:** Initialize Flet + Supabase connection. Verify Login.
2.  **The Reader:** Build the "Unified Timeline" fetching from `daily_mails` and `textbook_chapters`. Implement the "Kindle" styling.
3.  **The Workspace:** Build the logic to create folders/files and launch `code .`.
4.  **The Gamification:** Tie the "Run Tests" button to the XP system.

**Go.**
