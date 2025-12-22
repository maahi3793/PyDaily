import sys
import os
import argparse
import logging
import time

print("--- STARTUP DIAGNOSTICS ---")
print(f"CWD: {os.getcwd()}")
print(f"PYTHONPATH: {sys.path}")
print("ENV VARS AVAILABLE:", [k for k in os.environ.keys() if 'KEY' in k or 'CRED' in k or 'EMAIL' in k])
print("Checking backend/...", os.path.exists('backend'), os.path.exists('backend/__init__.py'))
print("---------------------------")

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
            if is_quiz_day:
                logging.info(f"🎯 Quiz Day detected: Generating Quiz for Day {day}...")
                history = cache.get_topics_history(day)
                content = gemini.generate_quiz(day, history)
            else:
                logging.info(f"Cache Miss: Generating Day {day} Lesson...")
                # Get history up to yesterday
                history = cache.get_topics_history(day - 1)
                content = gemini.generate_lesson(day, history)
            
            cache.save_lesson(day, content)
        
        # 2. Send
        subject = f"🎯 PyDaily Challenge: Day {day}" if is_quiz_day else f"🐍 PyDaily: Day {day}"
        success, msg = mailer.send_email(group, subject, content)
        
        if success:
            # 3. Update Status
            for student in group:
                data_manager.update_contact_status(student['email'], status='lesson_sent')
            logging.info(f"✅ Sent Day {day} to {len(group)} students.")
        else:
            logging.error(f"❌ Failed Day {day}: {msg}")

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
        if not content:
            logging.info(f"Cache Miss: Generating Day {day} Reminder...")
            content = gemini.generate_reminder(day)
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

def main():
    parser = argparse.ArgumentParser(description="PyDaily Automation Bot")
    parser.add_argument('--mode', choices=['morning', 'evening', 'motivation'], required=True, help="Mode to run: morning (Lessons), evening (Reminders), or motivation (Boost)")
    args = parser.parse_args()

    # Load Config
    config = data_manager.get_config()
    if not config.get('gemini_key') or not config.get('email_address'):
        logging.error("Configuration missing! Run the App UI to set keys.")
        return

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

if __name__ == "__main__":
    main()
