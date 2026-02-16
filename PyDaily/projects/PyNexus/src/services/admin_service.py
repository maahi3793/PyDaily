import sys
import os
import re
import logging
from pathlib import Path

# --- BRIDGE LOGIC: Allow imports from Sibling Projects ---
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent # relaunchpython
sys.path.append(str(project_root))

python_book_root = project_root / "PythonBook"
sys.path.append(str(python_book_root))

# --- LAZY IMPORTS (only load when needed) ---
_TextbookDB = None
_TextbookGenerator = None
_SupabaseManager = None

def _get_textbook_db():
    global _TextbookDB
    if _TextbookDB is None:
        from PythonBook.backend.db_textbook import TextbookDB
        _TextbookDB = TextbookDB()
    return _TextbookDB

def _get_supabase_manager():
    global _SupabaseManager
    if _SupabaseManager is None:
        from PyDailyEmail.backend.db_supabase import SupabaseManager
        _SupabaseManager = SupabaseManager()
    return _SupabaseManager

def _get_generator():
    global _TextbookGenerator
    if _TextbookGenerator is None:
        from PythonBook.backend.generator import TextbookGenerator
        _TextbookGenerator = TextbookGenerator()
    return _TextbookGenerator

class AdminService:
    def __init__(self):
        print("DEBUG: AdminService created (lazy mode)")
        # Don't initialize anything heavy here - use properties
        self._db = None
        self._supabase = None
        self._generator = None
        self._pending_images_cache = None
        
    @property
    def db(self):
        if self._db is None:
            self._db = _get_textbook_db()
        return self._db
    
    @property
    def supabase(self):
        if self._supabase is None:
            self._supabase = _get_supabase_manager()
        return self._supabase
    
    @property
    def generator(self):
        if self._generator is None:
            self._generator = _get_generator()
        return self._generator
        
    # --- ILLUSTRATOR FEATURES ---
    
    def get_pending_images(self):
        """Fetch all images marked as pending from textbook_images."""
        if self._pending_images_cache is None:
            self._pending_images_cache = self.db.get_pending_images()
        return self._pending_images_cache

    def get_days_with_pending_images(self):
        """Return unique list of days that have pending images."""
        images = self.get_pending_images()
        days = sorted(list(set(img['chapter_day'] for img in images)))
        return days
        
    def get_images_for_day(self, day):
        """Return pending images for a specific day."""
        all_imgs = self.get_pending_images()
        return [img for img in all_imgs if img['chapter_day'] == day]

    def upload_image(self, file_path, file_name, image_id):
        """
        Uploads a file to Supabase Storage 'textbook-images' bucket.
        Returns the Public URL.
        """
        if not self.supabase.admin_supabase:
            return None, "No Admin Key"
            
        try:
            # 1. Read binary
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # 2. Upload
            bucket = "textbook-images"
            storage_path = f"{image_id}_{file_name}"
            
            res = self.supabase.admin_supabase.storage.from_(bucket).upload(
                path=storage_path,
                file=file_data,
                file_options={"upsert": "true", "content-type": "image/png"}
            )
            
            # 3. Get Public URL
            public_url = self.supabase.admin_supabase.storage.from_(bucket).get_public_url(storage_path)
            
            return public_url, None
            
        except Exception as e:
            msg = str(e)
            print(f"Upload Failed: {msg}")
            return None, msg

    def inject_image(self, day, image_id, public_url):
        """
        Replaces the placeholder in 'daily_content' with the Markdown Image.
        """
        try:
            chapter = self.db.get_or_create_chapter(day)
            if not chapter:
                return False, "Chapter not found"
            
            parts_to_check = ['content_part1_theory', 'content_part2_practice', 'content_part3_mentor']
            updated = False
            
            placeholder_tag = f"<!-- IMAGE_PLACEHOLDER: {image_id} -->"
            
            for col in parts_to_check:
                content = chapter.get(col, "")
                if content and placeholder_tag in content:
                    img_record = self.db.client.table("textbook_images").select("description").eq("id", image_id).single().execute()
                    alt_text = img_record.data.get('description', 'Illustration') if img_record.data else "Illustration"
                    
                    new_image_md = f"![{alt_text}]({public_url})"
                    new_content = content.replace(placeholder_tag, new_image_md)
                    
                    self.db.update_chapter_part(day, col, new_content)
                    print(f"✅ Injected image {image_id} into Day {day} ({col})")
                    updated = True
                    
            if updated:
                self.db.update_image_url(image_id, public_url)
                # Clear cache
                self._pending_images_cache = None
                return True, "Image Infused Successfully"
            else:
                return False, "Placeholder not found in text"

        except Exception as e:
            return False, str(e)

    # --- EDITOR FEATURES ---
    
    def get_all_days(self):
        return list(range(1, 181)) # 1 to 180

    def regenerate_content(self, day, part):
        """
        Triggers the TextbookGenerator.
        """
        try:
            clean_part = part.lower()
            if "theory" in clean_part or "part 1" in clean_part: p = 'part1'
            elif "practice" in clean_part or "part 2" in clean_part: p = 'part2'
            elif "mentor" in clean_part or "part 3" in clean_part: p = 'part3'
            else: p = 'all'
            
            print(f"🔄 Triggering Regeneration: Day {day}, Part {p}")
            res = self.generator.generate_day(day, p)
            
            if res['success']:
                return True, res['message']
            else:
                return False, res['message']
                
        except Exception as e:
            return False, str(e)
