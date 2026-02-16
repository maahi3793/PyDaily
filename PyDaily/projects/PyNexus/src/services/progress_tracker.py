"""
ProgressTracker: Local storage for XP, completions, and retry counts.
Stores data in ~/.pynexus/progress.json
"""
import json
from pathlib import Path
from datetime import datetime, timedelta

class ProgressTracker:
    def __init__(self):
        self.pynexus_dir = Path.home() / ".pynexus"
        self.progress_file = self.pynexus_dir / "progress.json"
        self._ensure_dir()
        self.data = self._load()
    
    def _ensure_dir(self):
        if not self.pynexus_dir.exists():
            self.pynexus_dir.mkdir(parents=True)
    
    def _load(self) -> dict:
        """Load progress from disk."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"total_xp": 0, "completed": {}, "retries": {}, "in_progress": []}
    
    def _save(self):
        """Save progress to disk."""
        with open(self.progress_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    # ---- XP Methods ----
    def get_total_xp(self) -> int:
        return self.data.get("total_xp", 0)
    
    def add_xp(self, exercise_id: str, xp: int):
        """Add XP for completing an exercise."""
        self.data["total_xp"] = self.data.get("total_xp", 0) + xp
        self.data["completed"][exercise_id] = {
            "xp": xp,
            "completed_at": datetime.now().isoformat()
        }
        # Remove from in_progress if present
        if exercise_id in self.data.get("in_progress", []):
            self.data["in_progress"].remove(exercise_id)
        self._save()
    
    def is_completed(self, exercise_id: str) -> bool:
        return exercise_id in self.data.get("completed", {})
    
    # ---- Gamification Methods (New) ----
    def get_level(self) -> int:
        """Calculate level based on XP (1000 XP per level)."""
        return 1 + (self.get_total_xp() // 1000)

    def get_next_level_progress(self) -> tuple:
        """Returns (current_xp_in_level, xp_needed_for_next_level)."""
        total = self.get_total_xp()
        current_in_level = total % 1000
        return current_in_level, 1000

    def get_streak(self) -> int:
        """Calculate consecutive days of activity ending today or yesterday."""
        if not self.data.get("completed"):
            return 0
            
        completed_dates = set()
        for data in self.data["completed"].values():
            try:
                dt = datetime.fromisoformat(data["completed_at"])
                completed_dates.add(dt.date())
            except (ValueError, TypeError):
                continue
        
        if not completed_dates:
            return 0
            
        streak = 0
        today = datetime.now().date()
        
        # Check if activity today. If not, check yesterday.
        # If neither, streak is broken.
        check_date = today
        if check_date not in completed_dates:
            check_date = today - timedelta(days=1)
            if check_date not in completed_dates:
                return 0
        
        # Count backwards
        while check_date in completed_dates:
            streak += 1
            check_date -= timedelta(days=1)
            
        return streak

    # ---- Retry Methods ----
    def get_retries(self, exercise_id: str) -> int:
        return self.data.get("retries", {}).get(exercise_id, 0)
    
    def increment_retry(self, exercise_id: str):
        """Increment retry count on test failure."""
        if "retries" not in self.data:
            self.data["retries"] = {}
        self.data["retries"][exercise_id] = self.data["retries"].get(exercise_id, 0) + 1
        self._save()
    
    def reset_retries(self, exercise_id: str):
        """Reset retries on completion."""
        if exercise_id in self.data.get("retries", {}):
            del self.data["retries"][exercise_id]
            self._save()
    
    # ---- In Progress Tracking ----
    def mark_in_progress(self, exercise_id: str):
        """Mark an exercise as in progress."""
        if "in_progress" not in self.data:
            self.data["in_progress"] = []
        if exercise_id not in self.data["in_progress"]:
            self.data["in_progress"].append(exercise_id)
            self._save()
    
    def get_in_progress(self) -> list:
        return self.data.get("in_progress", [])
    
    def is_in_progress(self, exercise_id: str) -> bool:
        return exercise_id in self.data.get("in_progress", [])
