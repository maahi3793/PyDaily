# GitHub Actions Audit

## 1. PyDaily (Root)
**Repo**: `https://github.com/maahi3793/PyDaily` (main)
**Path**: `.github/workflows/`

| Workflow File | Trigger (Cron) | Time (UTC) | Time (IST) | Description |
| :--- | :--- | :--- | :--- | :--- |
| `daily_scheduler.yml` | `30 2 * * *` | 02:30 | **08:00 AM** | **Morning Cycle** (Morning Lessons) |
|                       | `30 5 * * *` | 05:30 | **11:00 AM** | **Quiz Insights** |
|                       | `30 6 * * *` | 06:30 | **12:00 PM** | **Motivation Boost** |
|                       | `30 14 * * *` | 14:30 | **08:00 PM** | **Evening Cycle** |
| `boss_scheduler.yml`  | `30 3 * * *` | 03:30 | **09:00 AM** | **Boss Battle Generation** |

---

## 2. PythonBook
**Path**: `PythonBook/.github/workflows/`

| Workflow File | Trigger (Cron) | Time (UTC) | Time (IST) | Description |
| :--- | :--- | :--- | :--- | :--- |
| `textbook_scheduler.yml` | `0 2 * * *` | 02:00 | **07:30 AM** | **Theory (Part 1)** |
|                          | `0 5 * * *` | 05:00 | **10:30 AM** | **Practice (Part 2)** |
|                          | `0 8 * * *` | 08:00 | **01:30 PM** | **Mentor (Part 3)** |
|                          | `0 11 * * *` | 11:00 | **04:30 PM** | **Batch Easy** |
|                          | `0 14 * * *` | 14:00 | **07:30 PM** | **Batch Medium** |
|                          | `0 17 * * *` | 17:00 | **10:30 PM** | **Batch Hard** |

---

## 3. Discrepancy Note: `PyDailyEmail`
There is a nested folder `PyDailyEmail` which is a **git submodule/clone** of `PyDaily`.
It contains:
- `PyDailyEmail/.github/workflows/boss_scheduler.yml`
This appears to be a **duplicate** or older version of the root `boss_scheduler.yml`. 
*Note: GitHub Actions will NOT run this file unless the `PyDailyEmail` folder is pushed as a separate root repository.*
