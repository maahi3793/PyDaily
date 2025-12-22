import os
import google.generativeai as genai
import logging

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

    def generate_lesson(self, day_number, history_context=None):
        logging.info(f"Attempting to generate lesson for Day {day_number}")
        
        context_str = ""
        if history_context:
            context_str = f"PREVIOUSLY COVERED TOPICS:\n{history_context}\n\nINSTRUCTION: Based on the above path, choose the NEXT logical topic for Day {day_number}."
        else:
            context_str = f"INSTRUCTION: This is the very first lesson (Day {day_number}). Start with the absolute basics (Installation/Intro)."

        try:
            prompt = f"""
            Generate the official PyDaily Newsletter for Day {day_number}.
            
            {context_str}
            
            CONTENT REQUIREMENTS:
            - Explain the topic clearly with analogies.
            - Provide code examples (Dark Mode).
            - Include a 'Daily Challenge'.

            STRICT FORMATTING RULES:
            1. INSERT THIS COMMENT AT THE VERY TOP (Crucial for tracking):
               <!-- TOPIC: [The Topic Name, e.g. Variables] -->

            2. Output VALID HTML matching this structure:
               <div style="font-family: Helvetica, Arial, sans-serif; max-width:600px; margin:0 auto; border:1px solid #e0e0e0; border-radius:10px;">
                 <div style="background-color:#3776AB; color:white; padding:20px; text-align:center; border-radius:10px 10px 0 0;">
                   <h2>🐍 PyDaily: Day {day_number}</h2>
                 </div>
                 <div style="padding:20px; color:#333;">
                    [Content...]
                    
                    <pre style="background-color:#2d2d2d; color:#f8f8f2; padding:15px; border-radius:5px; overflow-x:auto;"><code>
                    print("Code")
                    </code></pre>
                 </div>
                 <div style="background-color:#eee; padding:10px; text-align:center; font-size:12px; border-radius:0 0 10px 10px;">
                    Keep coding!
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
        logging.info(f"Attempting to generate EXTREME QUIZ for Day {day_number}")
        
        try:
            prompt = f"""
            Generate a SENIOR-LEVEL INTERVIEW QUIZ for a Python Developer.
            
            CONTEXT:
            The student has completed Days 1-{day_number}.
            Topics Covered So Far: {history_context}
            
            QUIZ REQUIREMENTS:
            - Total Questions: 15
            - Composition: 
                * 10 Multiple Choice Questions (Conceptual & Tricky)
                * 5 Code Snippet Analysis Questions ("What is the output?", "Find the bug")
            - Difficulty: "Real-life Interview" (3 Years Experience expectation). 
            - Style: Tricky edge cases, memory management, mutable defaults, shallow copies, etc. (relevant to covered topics).
            
            STRICT FORMATTING RULES:
            1. Output VALID HTML.
            2. Structure:
               <div style="font-family: Helvetica, Arial, sans-serif; max-width:600px; margin:0 auto; border:1px solid #e0e0e0; border-radius:10px;">
                 <div style="background-color:#4F46E5; color:white; padding:20px; text-align:center; border-radius:10px 10px 0 0;">
                   <h2>🎯 Interview Prep: Day {day_number}</h2>
                   <p>Level: 3 Years Experience</p>
                 </div>
                 <div style="padding:20px; color:#333;">
                    
                    <!-- Question Loop -->
                    <div style="margin-bottom:20px; border-bottom:1px solid #eee; padding-bottom:15px;">
                        <strong>Q1. [Question Text]</strong><br>
                        A) Option ...<br>
                        B) Option ...<br>
                        <details style="margin-top:10px; color:#4F46E5; cursor:pointer;">
                            <summary>View Answer</summary>
                            <strong>Answer: B</strong><br>
                            <em>Explanation: [Deep technical explanation]</em>
                        </details>
                    </div>
                    
                 </div>
                 <div style="background-color:#eee; padding:10px; text-align:center; font-size:12px; border-radius:0 0 10px 10px;">
                    Pass mark: 12/15. Good luck.
                 </div>
               </div>

            3. NO MARKDOWN. RETURN ONLY THE HTML STRING.
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Gemini API Error (Quiz): {str(e)}")
            return f"Error generating quiz: {str(e)}"

    def generate_reminder(self, day_number):
        logging.info(f"Attempting to generate REMINDER for Day {day_number}")
        try:
            prompt = f"""
            Generate a short, encouraging evening check-in email for Day {day_number}.

            CONTENT GOALS:
            - Ask if they finished the Challenge/Quiz?
            - Provide a tiny, 1-sentence "Pro Tip" related to Day {day_number}'s topic.
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
