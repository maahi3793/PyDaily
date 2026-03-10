import sys
import os

sys.path.append('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily')
from backend import config as config_loader
from backend.gemini_service import GeminiService
from backend.db_supabase import SupabaseManager
from backend import curriculum

db = SupabaseManager()
api_key = "dummy"
with open('c:/Users/reach/.gemini/antigravity/scratch/relaunchpython/PyDaily/.env', 'r') as f:
    for line in f:
        if 'GEMINI_API_KEY' in line:
            api_key = line.split('=')[1].strip().strip('"').strip("'")
            break

gemini = GeminiService(api_key)

day = 48
print(f"Testing Quiz Generation for Day {day}...")
recent_days = [day-2, day-1]
recent_topics = [f"Day {d}: {curriculum.TOPICS.get(d, 'Topic')}" for d in recent_days if d > 0]
all_prior_days = range(1, day-2)
cumulative_topics = [f"Day {d}: {curriculum.TOPICS.get(d, 'Topic')}" for d in all_prior_days if d > 0 and "Quiz" not in curriculum.TOPICS.get(d, "")]

print("Recent Topics:", recent_topics)
try:
    content = gemini.generate_quiz(day, recent_topics, cumulative_topics)
    print("SUCCESS!")
    print(content[:200])
except Exception as e:
    print(f"FAILED: {e}")
