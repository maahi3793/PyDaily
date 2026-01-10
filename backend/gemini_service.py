import os
import time
import google.generativeai as genai
import logging
import warnings

# Suppress Deprecation Warnings (valid until late 2026)
warnings.filterwarnings("ignore", category=FutureWarning)

# Setup Logging
logging.basicConfig(
    filename='pydaily.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GeminiService:
    def __init__(self, api_key):
        if not api_key:
            logging.error("GeminiService initialized without API Key")
            raise ValueError("API Key is missing")
        
        logging.info(f"Configuring Gemini with Key: {api_key[:5]}...{api_key[-3:]}")
        genai.configure(api_key=api_key)
        
        self.model_name = 'gemini-flash-latest'
        logging.info(f"Using Model: {self.model_name}")
        self.model = genai.GenerativeModel(self.model_name, system_instruction="""
You are "PyDaily", an enthusiastic, expert Python Tutor bot.

Your mission:
Teach Python from absolute zero to continuous expert mastery. There is no day limit.
Goal: Logically progress from basics to Data Structures & Algorithms, to advanced frameworks, to niche specializations.

Tone:
Friendly, Mentor-like, use emojis sparingly.
""")

    def generate_lesson(self, day_number, topic, phase, phase_goal, history_context=None):
        logging.info(f"Attempting to generate lesson for Day {day_number} on topic: {topic}")
        
        # 2. Build Context
        context_str = f"""
        TODAY'S TOPIC: {topic}
        PHASE {phase} GOAL: {phase_goal}
        
        PAST TOPICS (for internal context logic only):
        {history_context if history_context else "None (First Lesson)"}
        
        INSTRUCTION: Create a comprehensive, FUN, and detailed lesson about "{topic}".
        """
        
        # Debug Log
        print(f"🎨 Generating Content for Day {day_number}: {topic}")

        try:
            prompt = f"""
            Generate the official PyDaily Newsletter for Day {day_number}.
            
            {context_str}
            
            CONTENT REQUIREMENTS:
            - **Tone**: Enthusiastic, Emoji-Rich, Friendly, and "Bright". Use emojis frequently! 🌟
            - **Length**: COMPREHENSIVE (5-6 minute read). ~600-800 words of core lesson content. Do NOT skimp on the explanation.
            - **Structure**:
                1. **Introduction**: A high-energy hook.
                2. **The Concept**: Deep dive with analogies (Explain Like I'm Five).
                3. **Code Examples**: Clear, well-commented code.
                4. **Real World**: Why do we care?
                5. **Daily Challenge**: Small task.
                6. **Cumulative Practice**: The 5 extra problems.
            
            NEGATIVE CONSTRAINTS:
            - Do NOT mention "100 Days of Code".
            - Do NOT make up your own topic.
            - Do NOT list the specific "Past Topics" in the text (e.g. don't say "Combine with Variables, Loops..."). Just say "Combine with previous concepts."
            
            STRICT FORMATTING RULES:
            1. Output VALID HTML matching this structure:
               <div style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; max-width:600px; margin:0 auto; border:1px solid #e0e0e0; border-radius:12px; overflow:hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                 <!-- HEADER: Bright & Happy Gradient -->
                 <div style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color:white; padding:32px 24px; text-align:center;">
                   <div style="text-transform:uppercase; letter-spacing:1.5px; font-size:0.85rem; font-weight:700; color:rgba(255,255,255,0.9); margin-bottom:8px;">🚀 PyDaily &bull; Day {day_number}</div>
                   <h1 style="margin:0; font-size:1.8rem; font-weight:800; line-height:1.2; text-shadow: 0 2px 4px rgba(0,0,0,0.1); color:#ffffff;">{topic}</h1>
                 </div>
                 
                 <div style="padding:32px; color:#334155; line-height:1.7; font-size:16px;">
                    <!-- Insert Long, Emoji-Rich Content Here -->
                    [Content...]
                    
                    <pre style="background-color:#1e293b; color:#f8fafc; padding:15px; border-radius:8px; overflow-x:auto; border:1px solid #334155;"><code>
                    print("Code Example")
                    </code></pre>

                    <hr style="border:0; border-top:2px dashed #e2e8f0; margin:30px 0;">
                    
                    <h3 style="color:#4f46e5;">🏋️ Cumulative Practice (5 Problems)</h3>
                    <p><em>Combine what you learned today with your previous superpowers!</em></p>
                    <ol>
                        <li><strong>[Problem Title]</strong>: ...</li>
                    </ol>
                 </div>
                 
                 <div style="background-color:#f8fafc; padding:15px; text-align:center; color:#64748b; font-size:13px; border-top:1px solid #e2e8f0;">
                    Made with 🐍 and 💜 by PyDaily
                 </div>
               </div>

            3. NO MARKDOWN. RETURN ONLY THE HTML STRING.
            """
            response = self.model.generate_content(prompt)
            logging.info("Content generated successfully")
            return response.text
        except Exception as e:
            logging.error(f"Gemini API Error: {str(e)}")
            return f"Error generating content: {str(e)}"

    def generate_quiz(self, day_number, history_context):
        logging.info(f"Attempting to generate JSON QUIZ for Day {day_number}")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logging.info(f"Quiz Generation Attempt {attempt + 1}/{max_retries}")
                
                # Dynamic Prompt for Retry (vary slightly if needed, but standard is fine)
                prompt = f"""
                Generate a BEGINNER-FRIENDLY QUIZ for a Python Student.
                
                CONTEXT:
                The student has completed Days 1-{day_number - 1}.
                Topics Covered So Far: {history_context}
                
                QUIZ REQUIREMENTS:
                - **Difficulty**: Beginner to Intermediate (Focus on core understanding, not tricks).
                - **Format**: JSON (Strict Check).
                - **Questions**: EXACTLY 25 Total.
                - **Type**: 100% Multiple Choice (No open-ended).
                - **Content**: Mix of Theory (15) and Simple Code Output Prediction (10).
                
                JSON SCHEMA:
                {{
                    "title": "Day {day_number} Checkpoint",
                    "questions": [
                        {{
                            "id": 1,
                            "question": "What is the output of...",
                            "options": ["A) Error", "B) 10", "C) 20", "D) None"],
                            "answer": "B) 10", 
                            "explanation": "Because Python..."
                        }}
                    ]
                }}
                
                STRICT RULES:
                1. Return ONLY the raw JSON string.
                2. No Markdown formatting (```json).
                3. Ensure "options" is always a list of 4 distinct strings. DOES NOT ALLOW EMPTY STRINGS.
                4. "answer" must match one of the "options" exactly.
                5. double check that NO options are empty (e.g. "A) ").
                """
                
                response = self.model.generate_content(prompt)
                
                # Clean potential markdown
                text = response.text.strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                
                # Basic Validation: Check if it looks like JSON
                if not text.startswith("{") or not text.endswith("}"):
                    raise ValueError("Output is not valid JSON structure")

                # DEEP VALIDATION (The Fix for 'Empty Options')
                import json
                data = json.loads(text)
                questions = data.get('questions', [])
                
                if len(questions) != 25: # STRICT CHECK
                     raise ValueError(f"Incorrect question count: {len(questions)} (Expected 25)")
                
                for q in questions:
                    if not q.get('question'): raise ValueError("Empty Question Text")
                    options = q.get('options', [])
                    if len(options) != 4: raise ValueError(f"Question {q.get('id')} has {len(options)} options (Expected 4)")
                    for opt in options:
                        if len(opt.strip()) < 3: # "A) " is 3 chars. "A)" is 2. Empty string is 0.
                            raise ValueError(f"Empty or Malformed Option Detected: '{opt}'")
                
                logging.info("✅ Valid Quiz JSON Generated.")
                return text
                
            except Exception as e:
                logging.warning(f"Gemini Attempt {attempt+1} Failed Validation: {e}")
                time.sleep(2)
        
        # If we get here, all retries failed.
        logging.error("All Gemini Quiz Retries Failed.")
        raise Exception("Failed to generate Quiz after 3 attempts.")

    def generate_class_insights(self, quiz_results_list, topic_context):
        logging.info(f"Generating CLASS INSIGHTS for {len(quiz_results_list)} students")
        
        try:
            # Minify data to save token window
            # We need: Student Email (for mapping), and WRONG answers (for analysis)
            minified_data = []
            for res in quiz_results_list:
                # res structure: {'email': '...', 'score': 5, 'total': 10, 'answers_json': { '1': 'A', ...}, 'questions_context': ...}
                # Ideally, we pass the Question Text + Student Answer vs Correct Answer
                # For now, let's assume we pass a summary string if possible, OR we let Gemini infer from raw data if we pass the Quiz Context.
                # Simplest approach: Pass "Student X Analysis" string.
                minified_data.append({
                    "email": res.get('email'),
                    "score": f"{res.get('score')}/{res.get('total')}",
                    "wrong_answers": res.get('wrong_summary', 'Not specified') # We will calculate this before calling
                })
            
            prompt = f"""
            You are a Senior Python Instructor. 
            I have quiz results for {len(quiz_results_list)} students on the topic: "{topic_context}".
            
            DATA:
            {minified_data}
            
            TASK:
            1. Analyze each student's performance.
            2. Generate a 2-sentence "Remedial Tip" for EACH student based on their specific weak spots.
            3. If they got a high score (>= 80%), praise them and suggest an advanced topic.
            
            OUTPUT SCHEMA (JSON):
            {{
                "student_feedback": [
                    {{
                        "email": "student@example.com",
                        "subject": "Quick Tip based on your Quiz 💡",
                        "message": "Hey! Great job. I noticed you struggled with Loops. Remember that..."
                    }}
                ]
            }}
            
            STRICT JSON ONLY. NO MARKDOWN.
            """
            
            response = self.model.generate_content(prompt)
            text = response.text.replace('```json', '').replace('```', '').strip()
            return text
            
        except Exception as e:
            logging.error(f"Insight Gen Error: {e}")
            return '{"student_feedback": []}'

    def generate_reminder(self, day_number, topic_name="General Python"):
        logging.info(f"Attempting to generate REMINDER for Day {day_number} (Topic: {topic_name})")
        try:
            prompt = f"""
            Generate a short, encouraging evening check-in email for Day {day_number}.
            Current Topic: {topic_name}

            CONTENT GOALS:
            - Ask if they finished the Challenge/Quiz?
            - Provide a tiny, 1-sentence "Pro Tip" related to {topic_name}.
            - Motivate them for tomorrow.

            STRICT FORMATTING RULES:
            1. Output VALID HTML matching this structure:
               <div style="font-family: Helvetica, Arial, sans-serif; max-width:600px; margin:0 auto; border:1px solid #e0e0e0; border-radius:10px;">
                 <div style="background-color:#2c3e50; color:white; padding:15px; text-align:center; border-radius:10px 10px 0 0;">
                   <h3>🌙 Nightly Check-in: Day {day_number}</h3>
                 </div>
                 <div style="padding:20px; color:#333; background-color:#f9f9f9;">
                    [Insert Content Here...]
                 </div>
                 <div style="text-align:center; padding:15px;">
                    <a href="https://github.com/maahi3793/PyDaily" style="background-color:#27ae60; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">I'm Ready for Day {day_number + 1} 🚀</a>
                 </div>
               </div>

            2. NO MARKDOWN. RETURN ONLY THE HTML STRING.
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Gemini API Error (Reminder): {str(e)}")
            return f"Error generating reminder: {str(e)}"
            
    def generate_motivation(self):
        logging.info("Attempting to generate MID-DAY motivation")
        try:
            prompt = """
            Generate a short, powerful "Mid-Day Boost" email for coding students.
            
            CONTENT:
            - A punchy, famous quote about persistence, logic, or building things (e.g. Steve Jobs, Grace Hopper, Linus Torvalds).
            - A brief 2-sentence commentary: "It's noon. You might be stuck. That's part of the process. Keep going."
            
            STRICT FORMATTING:
            1. HTML Card format similar to above, but use an AMBER/ORANGE header (#F59E0B).
            2. Title: "⚡ Mid-Day Boost"
            3. NO MARKDOWN.
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Gemini API Error (Motivation): {str(e)}")
            return f"Error generating motivation: {str(e)}"
    def generate_linkedin_post(self, lesson_content):
        logging.info("Generating LinkedIn Post from Lesson Content...")
        try:
            prompt = f"""
            You are a Viral Social Media Manager for "PyDaily" (A Python Newsletter).
            
            INPUT CONTEXT (The Actual Lesson):
            {lesson_content[:4000]}  # Truncate to safety limit
            
            TASK:
            Create a LinkedIn Post based on the above lesson.
            
            STRUCTURE:
            1. HOOK: A viral opening line about the topic. 🤯
            2. THE MICRO-LESSON: clearly explain the concept or show the code snippet from the lesson. (Keep it short & readable).
            3. THE PITCH:
               - "This is just a sneak peek."
               - "Join our Free Newsletter to get these lessons daily." 📩
               - "Test your skills with our Interactive Quizzes." 🧠
            
            CALL TO ACTION (MUST INCLUDE):
            "👉 Start your 100-Day Journey for Free: https://pydaily.streamlit.app"
            
            STRICT FORMAT:
            Return ONLY the raw text for the post. Use Emojis (🚀, 🐍, 💡).
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logging.error(f"Gemini LinkedIn Gen Error: {e}")
            return "🚀 Another day, another Python concept mastered! Join the newsletter: https://pydaily.streamlit.app #Python"
