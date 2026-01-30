# 🛠️ PyDaily Maintenance Manual

## Quick Reference
| I want to... | See Section |
|--------------|-------------|
| Fix a broken bot run | [Bot Troubleshooting](#bot-troubleshooting) |
| Debug empty Feed | [Feed Troubleshooting](#feed-troubleshooting) |
| Add a new lesson topic | [Adding Content](#adding-content) |
| Promote a user to Admin | [Admin Commands](#admin-commands) |
| Understand the codebase | [Architecture](#architecture) |

---

## Architecture

```
PyDailyEmail/
├── streamlit_app.py     # Entry point (Routes to views)
├── run_bot.py           # Daily email automation (Morning/Evening cycles)
├── run_boss_cycle.py    # Weekly boss battle generation
│
├── backend/             # Core logic (NO UI)
│   ├── db_supabase.py   # Database operations (SupabaseManager)
│   ├── gemini_service.py# AI generation (Lessons, Quizzes)
│   ├── email_service.py # SendGrid email sender
│   ├── curriculum.py    # TOPICS dict (Day -> Topic mapping)
│   └── lesson_manager.py# Lesson caching/retrieval
│
├── views/               # Streamlit UI pages
│   ├── login.py         # Login/Signup
│   ├── admin/           # Admin dashboard (logs, users)
│   └── student/         # Student portal (dashboard, feed, quizzes)
│       └── components/  # Reusable UI widgets
│
├── tools/               # Admin utility scripts (run manually)
│   ├── generate_nuggets_v2.py  # Populate feed content
│   ├── factory_reset.py        # DANGER: Reset all students
│   └── promote_admin.py        # Make a user admin
│
└── assets/              # SQL migrations, static files
    ├── setup_feed.sql   # Feed table schema
    └── setup_bookmarks.sql
```

---

## Bot Troubleshooting

### "Bot didn't send emails this morning"
**Check the GitHub Action logs** (if using Actions) or your console output.

**Common Causes:**
1.  **Time window missed**: Bot only runs during specific hours (check `run_bot.py` time checks).
2.  **No eligible students**: All students might be on Quiz days or already received emails.
3.  **API key expired**: Check `SENDGRID_API_KEY` in your `.env` or Streamlit Secrets.

**Quick Test:**
```bash
python run_bot.py morning --dry-run  # If dry-run flag exists
# or
python run_bot.py morning  # Actually send emails (CAREFUL!)
```

### "Bot crashed with ImportError"
Usually means a file was deleted/renamed that's still imported.
```bash
python -c "import run_bot"  # Quick syntax check
```

---

## Feed Troubleshooting

### "Feed shows 'Caught up' with no content"
**Cause**: No nuggets exist in DB for user's current day.

**Debug Steps:**
1.  Check user's day in Supabase (`profiles` table).
2.  Check `feed_nuggets` table for that day.
3.  If empty, regenerate:
    ```bash
    python -c "from tools.generate_nuggets_v2 import run_v2; run_v2(1, 25)"
    ```

### "Feed shows broken HTML"
**Cause**: A nugget's `content` field has malformed HTML.
**Fix**: Edit the row directly in Supabase, or delete and regenerate.

---

## Adding Content

### Add a New Day's Topic
1.  Edit `backend/curriculum.py`.
2.  Add entry to `TOPICS` dict:
    ```python
    TOPICS = {
        ...
        181: "Recursion Revisited",  # New day!
    }
    ```
3.  The bot will auto-generate the lesson on the next run.

### Add Feed Nuggets for a Day
```bash
python -c "from tools.generate_nuggets_v2 import ensure_nuggets_for_day; ensure_nuggets_for_day(181)"
```

---

## Admin Commands

### Promote a User to Admin
```bash
python tools/promote_admin.py user@example.com
```

### Factory Reset (DANGER!)
Resets ALL students to Day 1. Use with extreme caution.
```bash
python tools/factory_reset.py --confirm
```

### Clear Old Motivations
```bash
python tools/clear_motivations.py
```

---

## Database Tables

| Table | Purpose |
|-------|---------|
| `profiles` | User data (email, day, role, streak) |
| `lessons` | Cached lesson HTML per day |
| `quizzes` | Generated quiz JSON per day |
| `quiz_attempts` | Student's quiz answers |
| `feed_nuggets` | TikTok-style feed content |
| `boss_battles` | Weekly challenge content |
| `activity_logs` | User actions (login, view, etc.) |
| `user_bookmarks` | Saved lessons |

---

## Need More Help?
1.  Check the console/logs for errors.
2.  Search this file for keywords.
3.  Check Supabase for missing data.
4.  Ask Claude/Gemini to analyze a stack trace.
