import sys
import os
import logging
import json
from unittest.mock import MagicMock

# Path Setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Mock genai module BEFORE importing gemini_service
sys.modules['google.generativeai'] = MagicMock()

from backend import gemini_service, curriculum

logging.basicConfig(level=logging.INFO)

def test_quiz_prompt_structure(day=6):
    # Redirect stdout to a file to avoid encoding errors in the console
    with open('quiz_test_output.txt', 'w', encoding='utf-8') as f:
        # Keep original stdout for recovery if needed, but we just print to 'f' manually or redirect sys.stdout
        sys.stdout = f
        
        try:
            print(f"🧪 Testing Quiz Prompt Generation for Day {day}")
            
            # Initialize Service with Dummy Key
            gemini = gemini_service.GeminiService("dummy_key")
            
            # Context Data
            recent_days = [day-2, day-1]
            recent_topics = [f"Day {d}: {curriculum.TOPICS.get(d, 'Topic')}" for d in recent_days if d > 0]
            
            all_prior_days = range(1, day-2)
            cumulative_topics = [f"Day {d}: {curriculum.TOPICS.get(d, 'Topic')}" for d in all_prior_days if d > 0 and "Quiz" not in curriculum.TOPICS.get(d, "")]
            
            print("\n--- CONTEXT ---")
            print(f"Recent (80%): {recent_topics}")
            print(f"Cumulative (20%): {cumulative_topics}")
            
            # Mock the model's generate_content method
            mock_response = MagicMock()
            mock_response.text = json.dumps({
                "title": f"Day {day} Quiz",
                "questions": [{"id": i, "question": "Q", "options": ["A) 1", "B) 2", "C) 3", "D) 4"], "answer": "A) 1"} for i in range(20)]
            })
            gemini.model.generate_content.return_value = mock_response

            # Call the method
            gemini.generate_quiz(day, recent_topics, cumulative_topics)
            
            # Verify the PROMPT
            args, _ = gemini.model.generate_content.call_args
            actual_prompt = args[0]
            
            print("\n--- PROMPT ANALYSIS ---")
            
            checks = [
                ("ALLOWED KNOWLEDGE BASE", True),
                ("STRICT TOPIC SOURCES", True),
                ("RECENT TOPICS (80% of Questions form here)", True),
                ("REVIEW TOPICS (20% of Questions form here)", True),
                ("Control Flow (If/Else)", False), # Should NOT be explicitly mentioned as a negative constraint anymore
                ("Loops (For/While)", True), # Should be mentioned in the generic 'specifically, do NOT use Loops' rule at the end
                ("Functions (Def)", True), # Same as above
                ("SCOPE CHECK", True),
                ("EXACTLY 20 Total", True),
                ('8 Questions: "Guess the Output"', True),
            ]
            
            all_passed = True
            for phrase, expected in checks:
                present = phrase in actual_prompt
                # For common terms like "Loops", simple substring search might yield True because of the generic rule.
                # That is expected behavior now.
                status = "✅" if present == expected else "❌"
                print(f"{status} Phrase '{phrase}': {'Found' if present else 'Not Found'} (Expected: {expected})")
                if present != expected:
                    all_passed = False
                    
            if all_passed:
                print("\n🎉 PROMPT VERIFIED: Positive scoping logic correctly injected.")
            else:
                print("\n💥 PROMPT VERIFICATION FAILED.")
                print("--- Full Prompt Dump ---")
                print(actual_prompt)
                
        except Exception as e:
            print(f"❌ Test Failed: {e}")
            import traceback
            traceback.print_exc(file=f)

if __name__ == "__main__":
    test_quiz_prompt_structure(6)
