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
Teach Python from absolute zero to expert in 100 days through a DAILY NEWSLETTER EMAIL.

Audience:
• Complete beginners
• No technical background
• Assume the reader knows NOTHING

Tone:
• Friendly, warm, encouraging
• Mentor-like, not robotic
• Conversational
• Use emojis sparingly but playfully 🐍✨

Daily Structure:
Generate ONE email per day based on the given Day number and Topic.

Curriculum Strategy:
• Day 1: Big picture — What is Python, how it talks to the computer, print()
• Later days should build progressively and logically
• ALWAYS explain new terms before using them

Teaching Style Rules:
• Use simple language
• Use analogies (e.g., “A variable is like a labeled box”)
• Explain WHY before HOW
• Make the learner feel confident, not overwhelmed

CRITICAL FORMAT RULES (EMAIL-READY):

1. Output ONLY the HTML BODY (no <html>, <head>, or <body> tags)
2. Wrap everything in:
   <div style="max-width:600px; margin:0 auto; padding:20px; border:1px solid #e0e0e0; border-radius:10px; font-family: Helvetica, Arial, sans-serif;">
3. Header banner:
   <div style="background-color:#3776AB; color:white; padding:15px; border-radius:10px 10px 0 0; text-align:center;">
4. Code blocks MUST use dark mode:
   <pre style="background-color:#2d2d2d; color:#f8f8f2; padding:15px; border-radius:5px; overflow-x:auto;"><code>
5. Highlight key terms using:
   <span style="background-color:#fff3cd; padding:2px 5px; border-radius:3px;">
6. NO markdown code fences (no ```)

STRICT CONTENT ORDER (DO NOT CHANGE):

1. Subject Line (catchy)
2. Greeting (warm welcome)
3. The Concept (WHY) – 100–150 words, with analogies
4. The Syntax (HOW) – simple rules
5. Code Example – commented, beginner-friendly
6. 🐍 Py-Fact – fun trivia
7. 🧠 Pop Quiz – 1 short question
8. 💪 Daily Challenge – 1 practical task

Code Rules:
• Keep examples minimal
• Comment every line
• Never assume prior knowledge
""")

    def generate_lesson(self, day_number):
        logging.info(f"Attempting to generate lesson for Day {day_number}")
        try:
            prompt = f"""
            Generate the official PyDaily Newsletter for Day {day_number}.

            CONTENT REQUIREMENTS:
            - Topic: Matches the curriculum for Day {day_number}.
            - Tone: Friendly, Mentor-like, use emojis 🐍.
            - Sections: Subject, Greeting, Concept (Analogy), Syntax, Code, Trivia, Pop Quiz, Challenge.

            STRICT FORMATTING RULES (DO NOT IGNORE):
            1. Output VALID HTML matching this structure:
               <div style="font-family: Helvetica, Arial, sans-serif; max-width:600px; margin:0 auto; border:1px solid #e0e0e0; border-radius:10px;">
                 <div style="background-color:#3776AB; color:white; padding:20px; text-align:center; border-radius:10px 10px 0 0;">
                   <h2>🐍 PyDaily: Day {day_number}</h2>
                 </div>
                 <div style="padding:20px; color:#333;">
                    [Insert Content Here using <p>, <b>, <ul> tags]
                    
                    <div style="background-color:#f8f9fa; border-left:4px solid #3776AB; padding:15px; margin:15px 0;">
                       <strong>💡 Concept:</strong> [Analogy Here]
                    </div>

                    <pre style="background-color:#2d2d2d; color:#f8f8f2; padding:15px; border-radius:5px; overflow-x:auto;"><code>
                    # Python Code Here (Dark Mode)
                    print("Hello World")
                    </code></pre>
                 </div>
                 <div style="background-color:#eee; padding:10px; text-align:center; font-size:12px; border-radius:0 0 10px 10px;">
                    Keep coding! - The PyDaily Team
                 </div>
               </div>

            2. NO MARKDOWN (No ```html or ```).
            3. RETURN ONLY THE HTML STRING.
            """
            response = self.model.generate_content(prompt)
            logging.info("Content generated successfully")
            return response.text
        except Exception as e:
            logging.error(f"Gemini API Error: {str(e)}")
            return f"Error generating content: {str(e)}"

    def generate_reminder(self, day_number):
        logging.info(f"Attempting to generate REMINDER for Day {day_number}")
        try:
            prompt = f"""
            Write a short, encouraging evening reminder email for a Python student who just finished Day {day_number}.
            Subject: Did you crush Day {day_number}? 🌙
            Content:
            - Ask if they finished the "Challenge" from this morning.
            - Ask if they solved the "Pop Quiz".
            - Give a tiny hint or fun fact related to Day {day_number}'s topic.
            - Keep it brief and emojis friendly.
            - Format: HTML Body.
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Gemini API Error (Reminder): {str(e)}")
            return f"Error generating reminder: {str(e)}"
