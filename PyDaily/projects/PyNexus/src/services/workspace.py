import os
import subprocess
import shutil
from pathlib import Path
from services.auth import AuthService

class WorkspaceService:
    def __init__(self):
        # Base workspace directory (e.g. ~/PyDaily)
        self.home = Path.home()
        self.workspace_root = self.home / "PyDaily"
        self.auth = AuthService()

    def ensure_workspace(self):
        if not self.workspace_root.exists():
            self.workspace_root.mkdir(parents=True)

    def start_job(self, day_number: int):
        """
        1. Create ~/PyDaily/DayXX_Job
        2. Fetch scaffolding from Supabase (or defaults)
        3. Write main.py and test_main.py
        4. Open VS Code
        """
        self.ensure_workspace()
        
        day_str = f"Day{day_number:02d}"
        job_dir = self.workspace_root / f"{day_str}_Job"
        
        # 1. Create Folder
        if not job_dir.exists():
            job_dir.mkdir()
            (job_dir / "tests").mkdir(exist_ok=True)
        
        # 2. Fetch Scaffolding (Mockd for now if table empty/missing)
        starter_code = "# Write your solution here\n\ndef solve():\n    pass"
        test_code = """def test_solve():
    from main import solve
    assert solve() is not None
"""
        
        # Try fetching from Supabase 'exercises'
        if self.auth.client:
           try:
               res = self.auth.client.table("exercises").select("*").eq("day_number", day_number).execute()
               if res.data and len(res.data) > 0:
                   ex = res.data[0]
                   if ex.get('starter_code'): starter_code = ex['starter_code']
                   if ex.get('test_code'): test_code = ex['test_code']
           except Exception as e:
               print(f"Could not fetch exercises: {e}")

        # 3. Write Files (Don't overwrite if user worked on it? Architecture Bible says 'App creates...' implies reset or init.
        # We will check if exists to be safe, or just overwrite main.py if empty.
        # For 'Job Simulator' vibe, maybe we enforce strict starter state. 
        # But let's be safe: Write only if not exists.
        main_py = job_dir / "main.py"
        if not main_py.exists():
            main_py.write_text(starter_code)
            
        test_py = job_dir / "tests" / "test_main.py"
        if not test_py.exists():
            test_py.write_text(test_code)

        # 4. Open VS Code
        try:
            # Code is usually in PATH.
            cmd = "code.cmd" if os.name == 'nt' else "code"
            subprocess.Popen([cmd, str(job_dir)], shell=False)
            return f"Job started at {job_dir}. Grid updated."
        except Exception as e:
            return f"Created {job_dir}, but failed to launch code: {e}"

    def run_tests(self, day_number: int):
        day_str = f"Day{day_number:02d}"
        job_dir = self.workspace_root / f"{day_str}_Job"
        
        if not job_dir.exists():
            return (False, "Job not started yet.")
            
        try:
            # Run pytest in the directory
            result = subprocess.run(
                ["pytest"], 
                cwd=str(job_dir), 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                return (True, "ALL SYSTEMS GREEN. Ticket Resolved.")
            else:
                return (False, f"Tests Failed.\n{result.stdout}\n{result.stderr}")
        except FileNotFoundError:
             return (False, "pytest not found. Is it installed?")
