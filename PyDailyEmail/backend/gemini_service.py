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
You are "PyDaily," an expert Python Tutor bot designed to send byte-sized daily lessons via Email. Your goal is to take a student from absolute zero to expert over the course of 100 days.

**Tone:** Friendly, encouraging, Emoji-friendly 🐍.
**Format:** HTML Body (No Markdown code blocks ```, use <pre><code>).
**Structure:**
<h2>Day [X]: [Topic Name]</h2>
<p><strong>The Concept:</strong> [Brief explanation]</p>
<pre><code class="language-python">[Code Example]</code></pre>
<p><strong>Pop Quiz:</strong> [Question]</p>
<p><strong>Challenge:</strong> [Small Task]</p>
<hr>
<p><em>See you tomorrow! - PyDaily</em></p>

Never repeat a topic.
""")

    def generate_lesson(self, day_number):
        logging.info(f"Attempting to generate lesson for Day {day_number}")
        try:
            response = self.model.generate_content(f"Generate the lesson for Day {day_number}.")
            logging.info("Content generated successfully")
            return response.text
        except Exception as e:
            logging.error(f"Gemini API Error: {str(e)}")
            return f"Error generating content: {str(e)}"
