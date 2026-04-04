import sys
import os
import argparse
import logging
import time
import datetime

# print("--- STARTUP DIAGNOSTICS ---")
# print(f"CWD: {os.getcwd()}")
# print(f"PYTHONPATH: {sys.path}")
# print("ENV VARS AVAILABLE:", [k for k in os.environ.keys() if 'KEY' in k or 'CRED' in k or 'EMAIL' in k])
# print("Checking backend/...", os.path.exists('backend'), os.path.exists('backend/__init__.py'))
# print("---------------------------")

try:
    from collections import defaultdict
    from backend import gemini_service, email_service, lesson_manager
    from backend.db_supabase import SupabaseManager
    from tools.generate_nuggets_v2 import ensure_nuggets_for_day
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
    """
    Day-based routing:
    - Saturday (weekday 5) → Send Weekly Digest
    - Sunday-Friday → Send Motivational Quote
    """
    import datetime
    from backend import curriculum
    
    today = datetime.date.today()
    
    # ========== DAY-BASED ROUTING ==========
    is_saturday = (today.weekday() == 5)
    logging.info(f"📅 Checking Cycle Date: {today} | Weekday: {today.weekday()} (Saturday={is_saturday})")
    
    if is_saturday:  # 5 = Saturday
        logging.info("✅ TRIGGER: Saturday Detected -> Weekly Digest Mode")
        _send_weekly_digest(mailer, curriculum, today)
    else:
        logging.info(f"⚡ TRIGGER: Weekday Detected -> Motivation Quote Mode")
        _send_motivation_quote(gemini, mailer, cache, today)


def _send_motivation_quote(gemini, mailer, cache, today):
    """Send AI-generated motivational quote to all active students."""
    today_str = today.isoformat()
    
    # Get or generate motivation
    content = cache.get_motivation(today_str)
    if not content:
        logging.info("Cache Miss: Generating Motivation...")
        content = gemini.generate_motivation()
        cache.save_motivation(today_str, content)
    
    # Target: Active students subscribed to morning emails
    db = SupabaseManager()
    contacts = db.admin_get_all_students()
    active_students = [c for c in contacts 
                       if c.get('status') in ['pending', 'lesson_sent'] 
                       and c.get('sub_morning', True) is True]
    
    if not active_students:
        logging.info("No active students for Motivation.")
        return

    logging.info(f"Sending motivation to {len(active_students)} students...")
    success_list, failure_list = mailer.send_email(active_students, "⚡ PyDaily: Mid-Day Boost", content)
    
    if success_list:
        logging.info(f"✅ Motivation sent to {len(success_list)} students.")
    if failure_list:
        logging.error(f"❌ Failed to send motivation to {len(failure_list)} students: {failure_list}")


def _send_weekly_digest(mailer, curriculum, today):
    """Send personalized Weekly Digest to all active students (Saturdays only)."""
    
    # 1. Get all active students
    db = SupabaseManager()
    contacts = db.admin_get_all_students()
    active_students = [c for c in contacts 
                       if c.get('status') in ['pending', 'lesson_sent'] 
                       and c.get('sub_morning', True) is True]
    
    if not active_students:
        logging.info("No active students for Weekly Digest.")
        return
    
    # ========== FIX #2: Quiz lookup by email (more reliable) ==========
    # Build a map of student email -> set of quiz days they've taken
    attempts_by_email = {}
    try:
        # Get all students first to build id->email map
        all_profiles = db.admin_supabase.table("profiles").select("id, email").execute()
        id_to_email = {p['id']: p['email'] for p in (all_profiles.data or [])}
        
        # Now get quiz attempts
        all_attempts = db.admin_supabase.table("quiz_attempts").select("student_id, day").execute()
        for att in (all_attempts.data or []):
            sid = att.get('student_id')
            email = id_to_email.get(sid)
            if email:
                if email not in attempts_by_email:
                    attempts_by_email[email] = set()
                attempts_by_email[email].add(att.get('day'))
    except Exception as e:
        logging.warning(f"Failed to load quiz attempts: {e}")
        attempts_by_email = {}
    
    week_start = today - datetime.timedelta(days=7)
    
    for student in active_students:
        current_day = student.get('day', 1)
        student_email = student.get('email', '')
        student_quizzes = attempts_by_email.get(student_email, set())
        
        # Calculate week range (last 7 days of lessons)
        week_start_day = max(1, current_day - 7)
        week_end_day = current_day - 1  # Up to yesterday
        
        # ========== FIX #4: Count total quizzes generated vs attempted ==========
        total_quizzes_generated = 0
        total_quizzes_attempted = 0
        for d in range(1, current_day):  # All days up to now
            topic = curriculum.TOPICS.get(d, "")
            if "Quiz" in topic:
                total_quizzes_generated += 1
                if d in student_quizzes:
                    total_quizzes_attempted += 1
        
        # Build "This Week" section
        this_week_html = ""
        for d in range(week_start_day, week_end_day + 1):
            topic = curriculum.TOPICS.get(d, f"Day {d}")
            is_quiz = "Quiz" in topic
            quiz_taken = d in student_quizzes
            
            if is_quiz:
                if quiz_taken:
                    this_week_html += f'''
                    <tr><td style="padding:12px 10px; border-bottom:1px solid #eee; background:#f0fdf4;">
                        <span style="color:#22c55e; font-weight:bold;">✓</span>
                        <span style="color:#333; margin-left:6px;">Day {d}:</span>
                        <span style="color:#22c55e; font-weight:600;">{topic}</span>
                        <br><span style="color:#22c55e; font-size:12px; margin-left:18px;">Great job!</span>
                    </td></tr>'''
                else:
                    this_week_html += f'''
                    <tr><td style="padding:12px 10px; border-bottom:1px solid #eee; background:#fef2f2;">
                        <span style="color:#ef4444; font-weight:bold;">○</span>
                        <span style="color:#333; margin-left:6px;">Day {d}:</span>
                        <span style="color:#ef4444; font-weight:600;">{topic}</span>
                        <br><span style="color:#ef4444; font-size:12px; margin-left:18px;">Give it a try!</span>
                    </td></tr>'''
            else:
                this_week_html += f'''
                <tr><td style="padding:12px 10px; border-bottom:1px solid #eee;">
                    <span style="color:#22c55e; font-weight:bold;">✓</span>
                    <span style="color:#333; margin-left:6px;">Day {d}:</span>
                    <span style="color:#555;">{topic}</span>
                </td></tr>'''
        
        # Build "Coming Up" section
        next_week_html = ""
        for d in range(current_day, min(current_day + 5, 300)):
            topic = curriculum.TOPICS.get(d, f"Day {d}")
            next_week_html += f'''
            <tr><td style="padding:12px 10px; border-bottom:1px solid #eee;">
                <span style="color:#4F46E5;">→</span>
                <span style="color:#333; margin-left:6px;">Day {d}:</span>
                <span style="color:#555;">{topic}</span>
            </td></tr>'''
        
        # Stats
        days_completed = current_day - 1
        streak = student.get('streak', 0)
        
        # ========== FIX #3: Mobile-friendly HTML (stacked stats) ==========
        email_body = f'''
        <div style="max-width:600px; margin:0 auto; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:#ffffff;">
            
            <!-- Header -->
            <div style="background:#4F46E5; padding:24px 20px; text-align:center;">
                <h1 style="margin:0; color:white; font-size:22px; font-weight:600;">PyDaily Weekly Digest</h1>
                <p style="margin:6px 0 0; color:rgba(255,255,255,0.8); font-size:13px;">{week_start.strftime('%b %d')} - {today.strftime('%b %d, %Y')}</p>
            </div>
            
            <!-- Greeting -->
            <div style="padding:20px;">
                <p style="margin:0; font-size:15px; color:#333;">Hey <strong>{{{{NAME}}}}</strong>,</p>
                <p style="margin:8px 0 0; font-size:14px; color:#555; line-height:1.5;">
                    Here's your weekly progress recap. Keep the momentum going!
                </p>
            </div>
            
            <!-- Stats Grid (Mobile Friendly - 2x2) -->
            <div style="padding:0 20px 20px;">
                <table width="100%" cellpadding="0" cellspacing="8" style="background:#f8fafc; border-radius:8px;">
                    <tr>
                        <td width="50%" style="background:#fff; border-radius:8px; padding:16px; text-align:center; border:1px solid #e2e8f0;">
                            <div style="font-size:28px; font-weight:700; color:#4F46E5;">{days_completed}</div>
                            <div style="font-size:11px; color:#64748b; margin-top:4px;">Days Completed</div>
                        </td>
                        <td width="50%" style="background:#fff; border-radius:8px; padding:16px; text-align:center; border:1px solid #e2e8f0;">
                            <div style="font-size:28px; font-weight:700; color:#22c55e;">{streak}</div>
                            <div style="font-size:11px; color:#64748b; margin-top:4px;">Day Streak</div>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2" style="background:#fff; border-radius:8px; padding:16px; text-align:center; border:1px solid #e2e8f0;">
                            <div style="font-size:28px; font-weight:700; color:#f97316;">{total_quizzes_attempted} <span style="font-size:16px; color:#94a3b8;">of</span> {total_quizzes_generated}</div>
                            <div style="font-size:11px; color:#64748b; margin-top:4px;">Quizzes Attempted</div>
                        </td>
                    </tr>
                </table>
            </div>
            
            <!-- This Week Section -->
            <div style="padding:0 20px 20px;">
                <h2 style="margin:0 0 12px; font-size:16px; color:#4F46E5; border-bottom:2px solid #4F46E5; padding-bottom:6px;">This Week</h2>
                <table width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;">{this_week_html}</table>
            </div>
            
            <!-- Coming Up Section -->
            <div style="padding:0 20px 20px;">
                <h2 style="margin:0 0 12px; font-size:16px; color:#4F46E5; border-bottom:2px solid #4F46E5; padding-bottom:6px;">Coming Up</h2>
                <table width="100%" cellpadding="0" cellspacing="0" style="font-size:14px;">{next_week_html}</table>
            </div>
            
            <!-- Pro Tips -->
            <div style="padding:0 20px 20px;">
                <div style="background:#fffbeb; border:1px solid #fcd34d; border-radius:8px; padding:16px;">
                    <h3 style="margin:0 0 10px; font-size:14px; color:#b45309;">Pro Tips</h3>
                    <ul style="margin:0; padding-left:18px; color:#78350f; font-size:13px; line-height:1.7;">
                        <li>Try <strong>Practice Programs</strong> in the dashboard.</li>
                        <li>Feeling confident? Try <strong>Boss Battles</strong>!</li>
                        <li>Check the <strong>Deep Dive Link</strong> at the end of each lesson.</li>
                    </ul>
                </div>
            </div>
            
            <!-- CTA Button -->
            <div style="padding:0 20px 24px; text-align:center;">
                <a href="https://pydaily.streamlit.app" style="background:#4F46E5; color:white; padding:14px 32px; text-decoration:none; border-radius:6px; font-weight:600; font-size:14px; display:inline-block;">View Dashboard</a>
            </div>
            
        </div>
        '''
        
        success_list, failure_list = mailer.send_email([student], "📅 Your Weekly Progress", email_body)
        if success_list:
            # We don't strictly update a 'status' for weekly, but we can log success
            logging.info(f"✅ Weekly Digest sent to {student['email']}")
        else:
            logging.error(f"❌ Failed Weekly Digest for {student['email']}: {failure_list}")

def run_morning_cycle(gemini, mailer, cache):
    logging.info("🌞 Starting Morning Cycle (Lessons)...")
    db = SupabaseManager()
    

    contacts = db.admin_get_all_students()
    # Logic: Status 'pending' means they need the day's content
    pending_contacts = [c for c in contacts if c.get('status') == 'pending']

    if not pending_contacts:
        logging.info("No students pending lessons.")
        return

    day_groups = group_contacts_by_day(pending_contacts)

    for day, group in day_groups.items():
        logging.info(f"Processing Day {day} for {len(group)} students...")
        
        # Import curriculum early so it's available for Deep Dive links even on Cache Hits
        from backend import curriculum

        # 1. Get/Generate Content
        content = cache.get_lesson(day)
        
        # Check Quiz Logic
        is_quiz_day = (int(day) % 3 == 0) and (int(day) > 0)
        
        if not content:
            try:
                if is_quiz_day:
                    logging.info(f"🎯 Quiz Day detected: Generating Quiz for Day {day}...")
                    
                    # Quiz scope: ONLY the 2 days leading up to the quiz
                    recent_days = [day-2, day-1]
                    recent_topics = [f"Day {d}: {curriculum.TOPICS.get(d, 'Topic')}" for d in recent_days if d > 0]
                    
                    try:
                        content = gemini.generate_quiz(day, recent_topics)
                    except Exception as quiz_err:
                        logging.error(f"⚠️ QUIZ GENERATION FAILED for Day {day}: {quiz_err}")
                        raise quiz_err  # Let outer handler skip this group — do NOT send fallback
                else:
                    logging.info(f"Cache Miss: Generating Day {day} Lesson...")
                    
                    # [FIX] Use Curriculum for Lesson Context too (Optional, but safer)
                    history_str = "; ".join([f"Day {d}: {curriculum.TOPICS.get(str(d), '')}" for d in range(1, day)])
                    
                    # Fetch Topic & Phase
                    if day <= 179:
                        # Ensure we always stringify keys as TOPICS might have int keys or string keys
                        # curriculum.py seems to use Integers for keys based on previous view
                        topic = curriculum.TOPICS.get(int(day), f"Day {day} Concept")
                    else:
                        # ... (Infinite Mode Logic remains similar, or we can stricter it later)
                        topic = cache.get_topic_for_day(day)
                        if not topic:
                            logging.info(f"🔮 Infinite Mode: Predicting Next Topic for Day {day}...")
                            past_topics = []
                            for d in range(day - 5, day):
                                t = cache.get_topic_for_day(d)
                                if not t and d <= 179:
                                    t = curriculum.TOPICS.get(d, "Python Basics")
                                if t:
                                    past_topics.append(t)
                            topic = gemini.predict_next_topic(past_topics)
                            logging.info(f"✨ AI Decided Next Topic: {topic}")

                    phase, phase_goal = curriculum.get_phase_info(int(day))
                    
                    # Correct Call Signature: day, topic, phase, goal, history
                    content = gemini.generate_lesson(day, topic, phase, phase_goal, history_context=history_str)
            except Exception as e:
                logging.error(f"❌ GENERATION FAILED for Day {day}: {e}")
                logging.warning("Skipping this group to prevent bad data. Will retry next run.")
                continue # Skip to next day group, do NOT save, do NOT send.
            
            # Double Check Content Validity
            if not content or "Error" in content[:20]: # Extra safety check
                 logging.error(f"❌ Invalid Content Generated for Day {day}. Aborting.")
                 continue

            cache.save_lesson(day, content)
            
            # 1.5 Auto-Generate Feed Nuggets for this Day if missing
            try:
                ensure_nuggets_for_day(day)
            except Exception as e:
                logging.warning(f"Failed to auto-generate feed for Day {day}: {e}")
        
        # 2. Send
        subject = f"🎯 PyDaily Challenge: Day {day}" if is_quiz_day else f"🐍 PyDaily: Day {day}"
        
        # FIX: For Quizzes, don't send the Raw JSON. Send a Dashboard Link.
        if is_quiz_day:
            email_body = f"""
            <div style="font-family:sans-serif; max-width:600px; margin:0 auto; padding:30px; border:1px solid #e0e0e0; border-radius:10px;">
                <h1 style="color:#4F46E5; text-align:center;">Quiz Time!</h1>
                <p style="font-size:16px; color:#333;">Hey <strong>{{{{NAME}}}}</strong>,</p>
                <p style="font-size:16px; color:#333; line-height:1.6;">
                    You've reached <strong>Day {day}</strong> — and you've been doing great! 
                    Today's a quick checkpoint to see how much you remember.
                </p>
                <div style="background:#f3f4f6; padding:20px; border-radius:8px; margin:20px 0; text-align:center;">
                    <p style="margin:0; color:#555;">Quizzes help lock in what you've learned.<br>No pressure — just practice!</p>
                </div>
                <div style="text-align:center;">
                    <a href="https://pydaily.streamlit.app" style="background-color:#4F46E5; color:white; padding:15px 30px; text-decoration:none; border-radius:5px; font-weight:bold; display:inline-block;">Take the Quiz</a>
                </div>
                <p style="margin-top:20px; font-size:13px; color:#888; text-align:center;">Takes about 10 minutes. You've got this!</p>
            </div>
            """
        else:
            # Wrap lesson content with personalized greeting
            greeting = """<div style="font-family:sans-serif; max-width:600px; margin:0 auto; padding:20px 0;">
                <p style="font-size:16px; color:#333; margin:0 0 20px;">Hey <strong>{{NAME}}</strong>, here's today's lesson:</p>
            </div>"""
            email_body = greeting + content
            
            # --- FEATURE: DEEP DIVE LINKS (Retroactive Injection) ---
            # Try to fetch a smart link for this day/topic
            # We use the topic from earlier variables (cached or new)
            try:
                # Need to lookup topic again if it wasn't fresh in this scope?
                # Actually 'topic' var is available from the if/else block above (lines 102/106)
                # But wait, if it was a Cache Hit (Line 89), 'topic' might not be defined in this scope!
                # We need to ensure we have the topic name.
                
                current_topic_name = curriculum.TOPICS.get(day, f"Day {day} Concept")
                # Overwrite if infinite mode logic had a better name? 
                # For safety, let's stick to curriculum or DB lookup.
                
                deep_dive = curriculum.get_deep_dive_attrs(day, current_topic_name)
                if deep_dive:
                    dd_url, dd_source = deep_dive
                    dd_html = mailer.get_deep_dive_html(dd_url, dd_source)
                    email_body += dd_html
            except Exception as e:
                logging.warning(f"Failed to inject Deep Dive link: {e}")
            # --------------------------------------------------------

        success_list, failure_list = mailer.send_email(group, subject, email_body)
        
        if success_list:
            # 3. Update Status
            db = SupabaseManager()
            for student in success_list:
                db.admin_update_student_progress(student['email'], status='lesson_sent')
            logging.info(f"✅ Sent Day {day} to {len(success_list)} students.")
        
        if failure_list:
            logging.error(f"❌ Failed Day {day} for {len(failure_list)} students. They will remain in PENDING. Errors: {failure_list}")

    # --- LINKEDIN AUTOMATION ---
    # (Scrapped: User declined Personal Profile posting)
    pass

def run_evening_cycle(gemini, mailer, cache):
    logging.info("🌙 Starting Evening Cycle (Reminders)...")
    db = SupabaseManager()
    contacts = db.admin_get_all_students()
    sent_contacts = [c for c in contacts if c.get('status') == 'lesson_sent']

    if not sent_contacts:
        logging.info("No students need reminders.")
        return

    day_groups = group_contacts_by_day(sent_contacts)

    from backend import curriculum # Import curriculum map
    
    for day, group in day_groups.items():
        try:
            logging.info(f"Processing Day {day} Reminders for {len(group)} students...")
            
            # Get Topic explicitly to avoid "hallucinations"
            topic = curriculum.TOPICS.get(day, "Python Concepts")

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
                # Fetch Next Topic for Accurate Teaser
                from backend import curriculum
                next_topic = curriculum.TOPICS.get(day + 1, "the next concept")
                
                if not is_stale: logging.info(f"Cache Miss: Generating Day {day} Reminder (Topic: {topic}, Next: {next_topic})...")
                
                try:
                    content = gemini.generate_reminder(day, topic_name=topic, next_topic_name=next_topic)
                    
                    # Force validation check explicitly here before proceeding
                    is_valid, err_msg = cache.validate_content(content)
                    if not is_valid:
                        raise ValueError(f"Content failed validation: {err_msg}")
                        
                    # Double check generated content
                    if f"Day {day}" not in content:
                        logging.warning(f"⚠️ Generated content missing 'Day {day}'. Appending header.")
                        # Force header just in case
                        content = f"<h3>🌙 Nightly Check-in: Day {day}</h3>\n" + content
                        
                    cache.save_reminder(day, content)
                except Exception as api_err:
                    logging.warning(f"⚠️ Gemini failed to generate reminder ({api_err}). Using Fallback Template.")
                    content = f"""
                    <div style="font-family: Helvetica, Arial, sans-serif; max-width:600px; margin:0 auto; border:1px solid #e0e0e0; border-radius:10px;">
                      <div style="background-color:#2c3e50; color:white; padding:15px; text-align:center; border-radius:10px 10px 0 0;">
                        <h3>🌙 Nightly Check-in: Day {day}</h3>
                      </div>
                      <div style="padding:20px; color:#333; background-color:#f9f9f9; line-height: 1.6;">
                         <p>Hey there!</p>
                         <p>Just checking in on your progress for <strong>Day {day}: {topic}</strong>.</p>
                         <p>If you haven't finished the challenge yet, no worries! Take your time. Tomorrow, we will be diving into <strong>{next_topic}</strong>, so get some rest and prepare for an awesome lesson.</p>
                      </div>
                      <div style="text-align:center; padding:15px;">
                         <a href="https://pydaily.streamlit.app" style="background-color:#27ae60; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">Go to Student Portal 🚀</a>
                      </div>
                    </div>
                    """
                    # Use DB directly to bypass the strict validation of save_reminder, or assume fallback is valid
                    # Assuming fallback is long enough and valid (it is)
                    db = SupabaseManager() # Ensure db in scope
                    db.save_daily_reminder(day, content)
            
            # 2. Send
            success_list, failure_list = mailer.send_email(group, f"🌙 PyDaily Check-in: Day {day}", content)
            
            if success_list:
                # 3. Update Status (Complete + Increment Day)
                db = SupabaseManager()
                for student in success_list:
                    db.admin_update_student_progress(student['email'], day=day+1, status='pending')
                logging.info(f"✅ Sent Day {day} Reminders to {len(success_list)} students. Promoted to Day {day+1}.")
            
            if failure_list:
                logging.error(f"❌ Failed Day {day} Reminders for {len(failure_list)} students. Errors: {failure_list}")
        except Exception as e:
            logging.error(f"⚠️ CRITICAL: Failed to process Evening Batch for Day {day}: {e}")
            logging.warning("Skipping this group. Check logs.")
            continue

def run_insights_cycle(gemini, mailer, cache):
    logging.info("🧐 Starting Insights Cycle (AI Feedback)...")
    
    # 1. Fetch Pending Results
    # We need DB access here. run_bot typically uses data_manager, expecting it to cover everything.
    # But db methods are in data_manager.db
    # 1. Fetch Pending Results
    from backend.db_supabase import SupabaseManager
    db = SupabaseManager()
         
    results = db.admin_get_worst_pending_attempts()
    
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
        all_students = db.admin_get_all_students()
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
                
                success_list, failure_list = mailer.send_email([{'email': email}], subject, html_body)
                if success_list:
                    # Mark feedback as sent
                    matched_sid = None
                    for va in valid_attempts:
                        if va['email'] == email:
                            matched_sid = va['student_id']
                            break
                    
                    if matched_sid:
                        db.admin_mark_feedback_sent(matched_sid, day)
                        logging.info(f"✅ Feedback sent to {email} for Day {day}.")
                else:
                    logging.error(f"❌ Failed AI Feedback for {email}: {failure_list}")
                
        except Exception as e:
            logging.error(f"Failed to process insights for Day {day}: {e}")

def main():
    parser = argparse.ArgumentParser(description="PyDaily Automation Bot")
    parser.add_argument('--mode', choices=['morning', 'evening', 'motivation', 'insights', 'regenerate'], required=True, help="Mode to run")
    parser.add_argument('--day', help="Specific Day ID (Required for regeneration)")
    args = parser.parse_args()

    # Load Config
    from backend import config as config_loader
    config = config_loader.get_config()
    
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
    elif args.mode == 'regenerate':
        if not args.day:
            logging.error("❌ You must specify --day for regeneration mode.")
            sys.exit(1)
        run_regeneration_cycle(int(args.day), gemini, mailer, cache)

def run_regeneration_cycle(day, gemini, mailer, cache):
    """
    Forcefully regenerates content for a specific Day.
    Updates DB/Cache.
    Does NOT email students (safety).
    """
    logging.info(f"🔄 FORCE REGENERATION: Day {day}...")
    from backend import curriculum

    # 1. Determine Type (Quiz vs Lesson)
    is_quiz_day = (day % 3 == 0) and (day > 0)
    
    content = None
    subject = ""
    
    try:
        if is_quiz_day:
            logging.info(f"🎯 Regenerating Quiz for Day {day}...")
            # Quiz scope: ONLY the 2 days leading up to the quiz
            recent_days = [day-2, day-1]
            recent_topics = [f"Day {d}: {curriculum.TOPICS.get(d, 'Topic')}" for d in recent_days if d > 0]
            
            content = gemini.generate_quiz(day, recent_topics)
            subject = f"🎯 [REGEN] Quiz Day {day}"
        else:
            logging.info(f"📘 Regenerating Lesson for Day {day}...")
            # Context Logic
            history_str = "; ".join([f"Day {d}: {curriculum.TOPICS.get(str(d), '')}" for d in range(1, day)])
            topic = curriculum.TOPICS.get(int(day), f"Day {day} Concept") # Try int key first
            if not topic or "Day" in topic: # Fallback
                 topic = curriculum.TOPICS.get(str(day), f"Day {day} Concept")

            phase, phase_goal = curriculum.get_phase_info(int(day))
            
            content = gemini.generate_lesson(day, topic, phase, phase_goal, history_context=history_str)
            subject = f"🐍 [REGEN] Lesson Day {day}"

        # 2. Save (Overwrite)
        if content and "Error" not in content[:20]:
            cache.save_lesson(day, content)
            logging.info(f"✅ Content Request Saved to DB for Day {day}.")
            
            # 3. Notify Admin (Confirmation)
            admin_email = mailer.admin_email
            if admin_email:
                mailer.send_email([{'email': admin_email}], subject, f"<h3>Regeneration Complete</h3><p>Day {day} has been updated in the database.</p><br><b>Preview:</b><br>{content[:500]}...")
                logging.info(f"📧 Confirmation sent to Admin: {admin_email}")
        else:
            logging.error("❌ Content generation returned empty or error.")

    except Exception as e:
        logging.error(f"❌ REGENERATION FAILED: {e}")

if __name__ == "__main__":
    main()
