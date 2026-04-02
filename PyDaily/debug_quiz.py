import logging
import sys
from backend.gemini_service import GeminiService
from backend import curriculum

# Setup basic logging to see Gemini's feedback
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_quiz_generation():
    gemini = GeminiService()
    day = 63
    
    # [FIX] Mirroring run_bot.py logic
    recent_days = [day-2, day-1]
    recent_topics = [f"Day {d}: {curriculum.TOPICS.get(d, 'Topic')}" for d in recent_days if d > 0]
    
    all_prior_days = range(1, day-2)
    cumulative_topics = [f"Day {d}: {curriculum.TOPICS.get(d, 'Topic')}" for d in all_prior_days if d > 0 and "Quiz" not in curriculum.TOPICS.get(d, "")]
    
    print(f"--- Debugging Day {day} Quiz Generation ---")
    print(f"Recent Topics: {recent_topics}")
    print(f"Cumulative Topics: {len(cumulative_topics)} items")
    
    try:
        print("Sending request to Gemini... (Expected 20 questions)")
        res = gemini.generate_quiz(day, recent_topics, cumulative_topics)
        print("✅ SUCCESS!")
        print(f"Questions Returned: {len(res.split('\"question\":')) - 1}") # Rough count
        print("First 200 chars:")
        print(res[:200])
    except Exception as e:
        print(f"❌ FAILURE: {e}")

if __name__ == "__main__":
    test_quiz_generation()
