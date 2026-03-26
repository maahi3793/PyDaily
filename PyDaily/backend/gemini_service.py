import os
import time
from google import genai
from google.genai import types
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
        self.client = genai.Client(api_key=api_key)
        
        self.model_name = 'gemini-2.5-flash'
        logging.info(f"Using Model: {self.model_name}")
        self.system_instruction = """
You are "PyDaily", an enthusiastic, expert Python Tutor bot.

Your mission:
Teach Python from absolute zero to continuous expert mastery. There is no day limit.
Goal: Logically progress from basics to Data Structures & Algorithms, to advanced frameworks, to niche specializations.

Tone:
Friendly, Mentor-like, use emojis sparingly.
"""

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
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                    )
                )
                logging.info("Content generated successfully")
                return response.text
            except Exception as e:
                logging.warning(f"Gemini API Error on Attempt {attempt+1}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)
        
        logging.error("All Gemini Lesson Retries Failed.")
        return "Error generating content: Max retries exceeded."

    def generate_quiz(self, day_number, recent_topics, cumulative_topics):
        logging.info(f"Attempting to generate JSON QUIZ for Day {day_number}")
        
        # Combine lists for a Master Scope
        all_allowed_topics = recent_topics + cumulative_topics
        scope_str = "\n".join([f"- {t}" for t in all_allowed_topics])

        max_retries = 3
        for attempt in range(max_retries):
            try:
                logging.info(f"Quiz Generation Attempt {attempt + 1}/{max_retries}")
                
                # Dynamic Prompt with Strict POSITIVE Constraints
                prompt = f"""
                You are a strict Exam Proctor generating a Python Quiz for a beginner student on Day {day_number}.
                
                *** CRITICAL SCOPE INSTRUCTION ***
                The student has ONLY learned the following topics. 
                You must NOT ask about anything outside this list. 
                If a concept is not listed below, it does not exist in the student's universe yet.
                
                ALLOWED KNOWLEDGE BASE:
                {scope_str}
                
                STRICT TOPIC SOURCES:
                1. RECENT TOPICS (80% of Questions form here): {recent_topics}
                2. REVIEW TOPICS (20% of Questions form here): {cumulative_topics}
                
                QUIZ SPECIFICATIONS:
                - **Total Questions**: EXACTLY 20.
                - **Format**: JSON.
                - **Question Types**:
                    - 12 Questions: Multiple Choice Theory/Concept Checks.
                    - 8 Questions: "Guess the Output" Code Snippets (Multiple Choice).
                - **Topic Distribution**:
                    - 16 Questions must test RECENT TOPICS.
                    - 4 Questions must test REVIEW TOPICS.
                
                JSON SCHEMA:
                {{
                    "title": "Day {day_number} Checkpoint",
                    "questions": [
                        {{
                            "id": 1,
                            "type": "theory",
                            "question": "What is the result of ...",
                            "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
                            "answer": "A) ...", 
                            "explanation": "..."
                        }}
                    ]
                }}
                
                STRICT RULES:
                1. Return ONLY the raw JSON string. No Markdown.
                2. Ensure "options" is a list of 4 distinct strings.
                3. "answer" must match one of the "options" exactly.
                4. **SCOPE CHECK**: Before generating a question, ask yourself: "Is the syntax/concept required to answer this found in the ALLOWED KNOWLEDGE BASE?" If no, discard it.
                5. specifically, do NOT use Loops or Functions unless "Loops" or "Functions" appear explicitly in the ALLOWED KNOWLEDGE BASE.
                """
                
                response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                )
            )
                
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
                
                if len(questions) != 20: # STRICT CHECK
                     raise ValueError(f"Incorrect question count: {len(questions)} (Expected 20)")
                
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
            1. Analyze each student's performance based on their wrong answers.
            2. Detect the exact, pin-point specific concept they struggled with based on their wrong answers (e.g., "List Slicing", "While Loops"). Explicitly tell them to "go through [Specific Topic Name] once again" in their message. 
            3. If they got a high score (>= 80%), praise them and offer a "Pro Tip" related to TODAY'S TOPIC.
            
            NEGATIVE CONSTRAINTS:
            - DO NOT suggest advanced topics like Generators, Decorators, or Classes if the topic is foundational.
            - Stick strictly to the scope of "{topic_context}".
            - Keep advice simple and encouraging.
            
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
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                )
            )
            text = response.text.replace('```json', '').replace('```', '').strip()
            return text
            
        except Exception as e:
            logging.error(f"Insight Gen Error: {e}")
            return '{"student_feedback": []}'

    def generate_reminder(self, day_number, topic_name="General Python", next_topic_name="Python Concepts"):
        logging.info(f"Attempting to generate REMINDER for Day {day_number} (Topic: {topic_name})")
        prompt = f"""
        Generate a short, encouraging evening check-in email for Day {day_number}.
        Current Topic: {topic_name}
        Tomorrow's Topic: {next_topic_name}
        
        CONTENT GOALS:
        - Ask if they finished the Challenge/Quiz?
        - Provide a 2-3 sentence "Pro Tip" related to {topic_name}.
        - Motivate them for tomorrow's topic: "{next_topic_name}". TEASE IT EXCITINGLY.
        - Ensure the email body is substantial (at least 2 paragraphs).

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
                <a href="https://pydaily.streamlit.app" style="background-color:#27ae60; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">Go to Student Portal 🚀</a>
             </div>
           </div>

        2. NO MARKDOWN. RETURN ONLY THE HTML STRING.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                    )
                )
                return response.text
            except Exception as e:
                logging.warning(f"Gemini API Error (Reminder) on Attempt {attempt+1}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(3)
                    
        return "Error generating reminder: Max retries exceeded."
            
    def generate_motivation(self):
        logging.info("Attempting to generate MID-DAY motivation")
        try:
            import random
            themes = [
                # Global / Universal Themes
                "Stoic Philosophy", "Space Exploration", "Nature & Growth", "Engineering Marvels",
                "Sports Psychology", "Scientific Discovery", "Art & Creativity", "The History of Computing",
                "Mountaineering & Endurance", "Jazz & Improperisation",
                
                # Indian Context Themes (Mixed In)
                "Indian Mathematics (Ramanujan)", "Ancient Wisdom (Yoga/Vedas)", 
                "ISRO & Frugal Innovation", "The Art of Practice (Abhyasa)"
            ]
            theme = random.choice(themes)
            
            prompt = f"""
            You are an AI generating a daily motivation email.
            
            THEME: {theme}.
            
            TASK:
            Generate a short, powerful "Mid-Day Boost" HTML email.
            
            CONTENT:
            - A punchy quote relating {theme} to coding/resilience.
            - A brief 2-sentence commentary.
            - Focus on a diverse mix of global/Indian voices.
            
            STRICT OUTPUT RULES:
            1. Return ONLY the HTML code.
            2. DO NOT include any markdown formatting (no ```html fences).
            3. DO NOT include comments, dividers, or metadata (like #### or ----).
            4. Start the output immediately with <div style="...">.
            
            HTML TEMPLATE:
            <div style="font-family: sans-serif; max-width:600px; margin:0 auto; padding:20px; border:1px solid #ddd; border-top: 5px solid #F59E0B; border-radius:8px;">
                <h2 style="color:#F59E0B; margin-top:0;">⚡ Mid-Day Boost</h2>
                <blockquote style="font-size:18px; font-style:italic; color:#333; margin:20px 0; border-left:4px solid #F59E0B; padding-left:15px;">
                    "INSERT QUOTE HERE"
                </blockquote>
                <p style="color:#555; line-height:1.6;">
                    INSERT COMMENTARY HERE.
                </p>
                <div style="margin-top:20px; font-size:12px; color:#888; text-align:center;">
                    PyDaily • {theme}
                </div>
            </div>
            """
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                )
            )
            # Extra safety: Clean markdown if it slips through
            text = response.text.replace('```html', '').replace('```', '').strip()
            return text
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
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                )
            )
            return response.text.strip()
            
        except Exception as e:
            logging.error(f"Gemini LinkedIn Gen Error: {e}")
            return "🚀 Another day, another Python concept mastered! Join the newsletter: https://pydaily.streamlit.app #Python"

    def generate_boss_battles(self, topic, day):
        logging.info(f"Generating BOSS BATTLES for topic: {topic} (Day {day})")
        
        # Guardrails based on Curriculum Progress
        constraints = ""
        if day < 10:
            constraints = """
            - **STRICT SYNTAX LIMIT**: Use ONLY Variables, Strings, Integers, and basic Math.
            - **FORBIDDEN**: NO Loops (for/while), NO Functions (def), NO Classes, NO Imports.
            - Focus on: Logic, String Manipulation (slicing), and Type Conversion.
            """
        elif day < 20:
             constraints = """
            - **STRICT SYNTAX LIMIT**: Loops (for/while) and Lists are ALLOWED.
            - **FORBIDDEN**: NO Functions (def), NO Classes.
            - Focus on: Iteration, List processing, and Control Flow (if/else).
            """
        elif day < 70:
             constraints = """
            - **STRICT SYNTAX LIMIT**: Functions (def) are ALLOWED.
            - **FORBIDDEN**: NO Classes (OOP).
            - Focus on: Modular code, Dictionary logic, and Error Handling.
            """
        else:
             constraints = "- Full Python Syntax Allowed (OOP, Classes, Decorators)."

        try:
            prompt = f"""
            You are a Supportive Senior Mentor creating "Boss Battle" Challenges.
            
            TOPIC: {topic}
            DAY: {day} (Student Learning Phase)
            
            GOAL:
            Create 5 "Job-Ready" Coding Challenges. 
            They should be strictly constrained (to force creative thinking) but effectively SOLVABLE and ENCOURAGING.
            Do NOT make them "Google Interview" hard. Make them "Real Work" hard.
            
            CURRICULUM CONSTRAINTS (MUST FOLLOW):
            {constraints}
            
            GENERAL CONSTRAINTS:
            - **Tone**: Fun, encouraging, slightly gamified ("You are saving the database!").
            - **Forbidden Themes**: No Blockchain, No Cryptography, No Advanced Math, No Abstract Algorithms.
            - **Preferred Contexts**: Data Cleaning, Text Formatting, Log Parsing, Simple Game Logic, Inventory Management.
            - **Difficulty**: Challenging due to *constraints*, not due to *obscure logic*.
            
            OUTPUT SCHEMA (JSON Array):
            [
                {{
                    "title": "Clean the User Logs",
                    "scenario": "You are a Junior Dev. The server logs are messy. Extract the usernames...",
                    "requirements": [
                        "Input is a raw string...",
                        "Output must be a clean list..."
                    ],
                    "hints": [
                        "Try splitting the string by spaces first."
                    ]
                }}
            ]
            
            STRICT RULES:
            1. Return ONLY the JSON Array.
            2. Generate exactly 5 Battles.
            3. Ensure valid JSON.
            """
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                )
            )
            text = response.text.replace('```json', '').replace('```', '').strip()
            
            import json
            # Validation check
            data = json.loads(text)
            if not isinstance(data, list) or len(data) < 1:
                raise ValueError("Invalid Boss Battle JSON")
            
            return data
        except Exception as e:
            logging.error(f"Boss Battle Gen Error: {e}")
            return []
