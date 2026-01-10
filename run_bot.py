import sys
import os
import argparse
import logging
import time

# print("--- STARTUP DIAGNOSTICS ---")
# print(f"CWD: {os.getcwd()}")
# print(f"PYTHONPATH: {sys.path}")
# print("ENV VARS AVAILABLE:", [k for k in os.environ.keys() if 'KEY' in k or 'CRED' in k or 'EMAIL' in k])
# print("Checking backend/...", os.path.exists('backend'), os.path.exists('backend/__init__.py'))
# print("---------------------------")

try:
    from collections import defaultdict
    from backend import data_manager, gemini_service, email_service, lesson_manager
except ImportError as e:
    print(f"!!! CRITICAL IMPORT ERROR !!!: {e}")
    print("Files in current dir:", os.listdir('.'))
    if os.path.exists('backend'):
        print("Files in backend/:", os.listdir('backend'))
    sys.exit(1)

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def group_contacts_by_day(contact_list):
    groups = defaultdict(list)
    for c in contact_list:
        groups[c['day']].append(c)
    return groups

    if args.mode == 'morning':
        run_morning_cycle(gemini, mailer, cache)
    elif args.mode == 'evening':
        run_evening_cycle(gemini, mailer, cache)
    elif args.mode == 'motivation':
        run_motivation_cycle(gemini, mailer, cache)

def run_motivation_cycle(gemini, mailer, cache):
    logging.info("⚡ Starting Mid-Day Motivation Cycle...")
    import datetime
    today_str = datetime.date.today().isoformat()
    
    # 1. Get/Generate
    content = cache.get_motivation(today_str)
    if not content:
        logging.info("Cache Miss: Generating Motivation...")
        content = gemini.generate_motivation()
        cache.save_motivation(today_str, content)
    
    # 2. Target Audience: Everyone Active (Pending or Sent)
    contacts = data_manager.get_contacts()
    active_students = [c for c in contacts if c.get('status') in ['pending', 'lesson_sent']]
    
    if not active_students:
        logging.info("No active students for motivation.")
        return

    logging.info(f"Sending motivation to {len(active_students)} students...")
    success, msg = mailer.send_email(active_students, "⚡ PyDaily: Mid-Day Boost", content)
    
    if success:
        logging.info("✅ Motivation sent successfully.")
    else:
        logging.error(f"❌ Failed to send motivation: {msg}")

def run_morning_cycle(gemini, mailer, cache):
    logging.info("🌞 Starting Morning Cycle (Lessons)...")
    contacts = data_manager.get_contacts()
    # Logic: Status 'pending' means they need the day's content
    pending_contacts = [c for c in contacts if c.get('status') == 'pending']

    if not pending_contacts:
        logging.info("No students pending lessons.")
        return

    day_groups = group_contacts_by_day(pending_contacts)

    for day, group in day_groups.items():
        logging.info(f"Processing Day {day} for {len(group)} students...")

        # 1. Get/Generate Content
        content = cache.get_lesson(day)
        
        # Check Quiz Logic
        is_quiz_day = (int(day) % 3 == 0) and (int(day) > 0)
        
        if not content:
            try:
                if is_quiz_day:
                    logging.info(f"🎯 Quiz Day detected: Generating Quiz for Day {day}...")
                    history = cache.get_topics_history(day)
                    content = gemini.generate_quiz(day, history)
                else:
                    logging.info(f"Cache Miss: Generating Day {day} Lesson...")
                    history = cache.get_topics_history(day - 1)
                    from backend import curriculum
                    phase, phase_goal = curriculum.get_phase_info(int(day))
                    content = gemini.generate_lesson(day, history, phase, phase_goal)
            except Exception as e:
                logging.error(f"❌ GENERATION FAILED for Day {day}: {e}")
                logging.warning("Skipping this group to prevent bad data. Will retry next run.")
                continue # Skip to next day group, do NOT save, do NOT send.
            
            # Double Check Content Validity
            if not content or "Error" in content[:20]: # Extra safety check
                 logging.error(f"❌ Invalid Content Generated for Day {day}. Aborting.")
                 continue

            cache.save_lesson(day, content)
        
        # 2. Send
        subject = f"🎯 PyDaily Challenge: Day {day}" if is_quiz_day else f"🐍 PyDaily: Day {day}"
        
        # FIX: For Quizzes, don't send the Raw JSON. Send a Dashboard Link.
        if is_quiz_day:
            email_body = f"""
            <div style="font-family:sans-serif; max-width:600px; margin:0 auto; text-align:center; padding:30px; border:1px solid #e0e0e0; border-radius:10px;">
                <h1 style="color:#4F46E5;">⚔️ It's Quiz Day!</h1>
                <p style="font-size:18px; color:#333;">You have reached <strong>Day {day}</strong>. It's time to test your knowledge.</p>
                <div style="background:#f3f4f6; padding:20px; border-radius:8px; margin:20px 0;">
                    <p>This is an internal checkpoint. Log in to the Student Dashboard to take your Interactive Quiz.</p>
                </div>
                <a href="https://pydaily.streamlit.app" style="background-color:#4F46E5; color:white; padding:15px 30px; text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block;">👉 Go to Dashboard</a>
                <p style="margin-top:20px; font-size:12px; color:#888;">Complete this quiz to unlock tomorrow's lesson.</p>
            </div>
            """
        else:
            email_body = content

        success, msg = mailer.send_email(group, subject, email_body)
        
        if success:
            # 3. Update Status
            for student in group:
                data_manager.update_contact_status(student['email'], status='lesson_sent')
            logging.info(f"✅ Sent Day {day} to {len(group)} students.")
        else:
            logging.error(f"❌ Failed Day {day}: {msg}")

    # --- LINKEDIN AUTOMATION ---
    # (Scrapped: User declined Personal Profile posting)
    pass

def run_evening_cycle(gemini, mailer, cache):
    logging.info("🌙 Starting Evening Cycle (Reminders)...")
    contacts = data_manager.get_contacts()
    sent_contacts = [c for c in contacts if c.get('status') == 'lesson_sent']

    if not sent_contacts:
        logging.info("No students need reminders.")
        return

    day_groups = group_contacts_by_day(sent_contacts)

    for day, group in day_groups.items():
        logging.info(f"Processing Day {day} Reminders for {len(group)} students...")

        # 1. Get/Generate Content
        content = cache.get_reminder(day)
        
        # VALIDATION: Check if content matches the Day (Ref Issue: "11th day getting 10th day mail")
        # If the content explicitly mentions "Day X" and X != day, force regen.
        is_stale = False
        if content:
            if f"Day {day}" not in content and f"Day {day-1}" in content:
                logging.warning(f"⚠️ Stale/Invalid Reminder Detected for Day {day} (Found 'Day {day-1}'). forcing Regen.")
                is_stale = True
        
        if not content or is_stale:
            if not is_stale: logging.info(f"Cache Miss: Generating Day {day} Reminder...")
            content = gemini.generate_reminder(day)
            
            # Double check generated content
            if f"Day {day}" not in content:
                logging.warning(f"⚠️ Generated content missing 'Day {day}'. Appending header.")
                # Force header just in case
                content = f"<h3>🌙 Nightly Check-in: Day {day}</h3>\n" + content
                
            cache.save_reminder(day, content)
        
        # 2. Send
        success, msg = mailer.send_email(group, f"🌙 PyDaily Check-in: Day {day}", content)
        if success:
            # 3. Update Status (Complete + Increment Day)
            for student in group:
                data_manager.update_contact_status(student['email'], day=day+1, status='pending')
            logging.info(f"✅ Sent Day {day} Reminders. Students promoted to Day {day+1}.")
        else:
            logging.error(f"❌ Failed Day {day} Reminders: {msg}")

def run_insights_cycle(gemini, mailer, cache):
    logging.info("🧐 Starting Insights Cycle (AI Feedback)...")
    
    # 1. Fetch Pending Results
    # We need DB access here. run_bot typically uses data_manager, expecting it to cover everything.
    # But db methods are in data_manager.db
    from backend import data_manager
    if not hasattr(data_manager, 'db'):
         # Fallback if I didn't verify data_manager exposure perfectly? 
         # I did add 'db' to data_manager.py earlier.
         pass
         
    results = data_manager.db.admin_get_worst_pending_attempts()
    
    if not results:
        logging.info("No pending quiz attempts found for analysis.")
        return
        
    logging.info(f"Found {len(results)} pending quiz attempts (Worst scenarios selected).")
    
    # 2. Group by Day (To generate context-aware insights)
    day_groups = defaultdict(list)
    for r in results:
        day_groups[r['day']].append(r)
        
    # 3. Process Each Day
    for day, day_results in day_groups.items():
        logging.info(f"Analyzing Day {day} Attempts ({len(day_results)} students)...")
        
        # Get Topic Context
        from backend import curriculum
        topic = curriculum.TOPICS.get(day, "Python Concepts")
        
        # 4. Inject Emails
        all_students = data_manager.db.admin_get_all_students()
        id_to_email = {s['id']: s['email'] for s in all_students}
        
        valid_attempts = []
        for att in day_results:
            sid = att.get('student_id')
            email = id_to_email.get(sid)
            if email:
                att['email'] = email
                valid_attempts.append(att)
            else:
                logging.warning(f"Could not find email for student ID {sid}")
        
        if not valid_attempts:
            continue
            
        # 5. Call Gemini
        raw_json = gemini.generate_class_insights(valid_attempts, topic)
        
        import json
        try:
            data = json.loads(raw_json)
            feedback_list = data.get('student_feedback', [])
            
            for item in feedback_list:
                email = item.get('email')
                if not email: continue
                
                # Send Email
                html_body = f"""
                <div style="font-family:sans-serif; padding:15px; border-left:4px solid #4F46E5; background:#f9fafb;">
                    <h3>💡 Quick Tip: Day {day}</h3>
                    <p>{item['message']}</p>
                    <hr>
                    <p style="font-size:12px; color:#666;">This tip was generated by your AI Tutor based on your quiz performance. (We analyzed your toughest attempt to give the best advice!)</p>
                </div>
                """
                
                subject = f"Feedback on Day {day}: {item.get('subject', 'Keep going!')}"
                
                success, msg = mailer.send_email([{'email': email}], subject, html_body)
                
                if success:
                    # Mark as Sent
                    matched_sid = None
                    for va in valid_attempts:
                        if va['email'] == email:
                            matched_sid = va['student_id']
                            break
                    
                    if matched_sid:
                        data_manager.db.admin_mark_feedback_sent(matched_sid, day)
                        logging.info(f"✅ Feedback sent to {email} for Day {day}.")
                
        except Exception as e:
            logging.error(f"Failed to process insights for Day {day}: {e}")

def main():
    parser = argparse.ArgumentParser(description="PyDaily Automation Bot")
    parser.add_argument('--mode', choices=['morning', 'evening', 'motivation', 'insights'], required=True, help="Mode to run: morning (Lessons), evening (Reminders), motivation (Boost), or insights (AI Feedback)")
    args = parser.parse_args()

    # Load Config
    config = data_manager.get_config()
    
    # --- DEBUG SECTION ---
    print("--- ENV DEBUG ---")
    print(f"SUPABASE_URL Detected: {'YES' if config.get('supabase_url') else 'NO'}")
    if config.get('supabase_url'):
        print(f"SUPABASE_URL Length: {len(config.get('supabase_url'))}")
    
    masked_env = {}
    for k, v in os.environ.items():
        if 'KEY' in k or 'SECRET' in k or 'PASSWORD' in k:
            masked_env[k] = '***'
        elif 'URL' in k:
             masked_env[k] = v[:8] + '...' if v else 'EMPTY'
        else:
            masked_env[k] = v
    print("Full Env Keys:", sorted(masked_env.keys()))
    print("-----------------")

    if not config.get('gemini_key') or not config.get('email_address') or not config.get('supabase_url'):
        logging.error("Configuration missing! Checking: Gemini, Email, Supabase URL.")
        sys.exit(1)

    # Init Services
    gemini = gemini_service.GeminiService(config['gemini_key'])
    mailer = email_service.EmailService(
        config['email_address'], 
        config['email_password'],
        test_mode=config.get('test_mode', False),
        admin_email=config.get('admin_email', '')
    )
    cache = lesson_manager.LessonManager()

    if args.mode == 'morning':
        run_morning_cycle(gemini, mailer, cache)
    elif args.mode == 'evening':
        run_evening_cycle(gemini, mailer, cache)
    elif args.mode == 'motivation':
        run_motivation_cycle(gemini, mailer, cache)
    elif args.mode == 'insights':
        run_insights_cycle(gemini, mailer, cache)

if __name__ == "__main__":
    main()
