# Enterprise Document Intelligence Platform (Enterprise Doc Intel)

Welcome to the **Enterprise Document Intelligence Platform**! 

This is a secure, AI-powered tool designed to help you "chat" with your own private documents. Whether you have a massive PDF textbook, a collection of company policies, or lengthy reports, this platform allows you to ask questions and instantly get accurate answers based *strictly* on what is written in your files.

## 🌟 What It Is

Think of this platform as a super-smart, private librarian for your files. Instead of manually reading through hundreds of pages to find a specific fact, you simply upload the document and ask a question. The system reads the document, finds the exact paragraphs that contain the answer, and uses AI to summarize it for you.

## 🚀 What It Does (Key Features)

* **Private & Secure:** The heavy lifting of reading and indexing your documents happens locally on your own computer.
* **Strictly Factual:** The AI is strictly instructed to answer *only* using the documents you provided. It will not make up answers (hallucinate) or use outside knowledge.
* **Cost-Effective:** Instead of sending an entire 500-page book to an AI (which costs a lot of money/tokens), this platform only sends the 2 or 3 paragraphs that are actually relevant to your question.
* **Model Flexible:** You can choose the "Brain" you want to use. We currently support Google's **Gemini** and OpenAI's **GPT-4o Mini**.

---

## 📖 How to Use It (Zero Tech Knowledge Required!)

Follow these simple steps to get started:

### Step 1: Get an API Key (Your Secret Password)
To use the AI brain, you need a secret "API Key". You can get a free one from Google AI Studio, or use a paid one from OpenAI (ChatGPT).
* **For Google (Free):** Go to [Google AI Studio](https://aistudio.google.com/), sign in, and click "Get API key".
* **For OpenAI (Paid, but very cheap):** Go to [OpenAI Platform](https://platform.openai.com/), add a small amount of billing credit (e.g., $5), and generate a secret key (`sk-...`).

### Step 2: Configure Your Settings
1. Open the application in your web browser (usually at `http://localhost:3000`).
2. On the left-hand menu, click on **Settings**.
3. Paste your secret API key into the correct box (Gemini for Google, or OpenAI for ChatGPT).
4. Select the AI Model you want to use from the choices provided. *(Note: If you have a brand-new free Google account, select **Gemini Flash (Latest)** for the smoothest experience).*
5. Click **Save & Apply Settings**.

### Step 3: Upload Your Document
1. On the left-hand menu, click on **Uploads**.
2. Click the file upload box and select a document from your computer (PDFs, Word Documents, or Text files all work great).
3. Click the **Start Embedding** button.
4. *Wait a few seconds!* The system is reading and chopping up your document so it can be searched quickly. You will see a success message when it is done.

### Step 4: Ask Questions!
1. On the left-hand menu, click on **Query Console**.
2. Type your question into the search bar at the bottom. For example: *"What is the main topic of chapter 1?"* or *"Summarize the company's vacation policy."*
3. Click **Analyze**.
4. The AI will retrieve the correct information from your uploaded document and type out the answer for you!

---

## 🛠️ For the Technical Folks (How to start the app)

If you have just cloned this repository from GitHub, you need to install the dependencies first because `node_modules` and Python environments are ignored by Git.

**0. Install Dependencies (First Time Only):**
Open a terminal in the `backend` folder and run:
`pip install -r requirements.txt`

Open a terminal in the `frontend` folder and run:
`npm install`

**1. Start the Backend (The Data Engine):**
Open a terminal, navigate to the `backend` folder, and run:
`uvicorn main:app --port 8000`

**2. Start the Frontend (The User Interface):**
Open a second terminal, navigate to the `frontend` folder, and run:
`npm run dev`

Then, open your web browser and go to `http://localhost:3000`.
