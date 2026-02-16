import os
import subprocess
import shutil
import re
from pathlib import Path

class Scaffolder:
    def __init__(self):
        # Dedicated Practice Directory
        self.home = Path.home()
        self.practice_root = self.home / "PyNexus_Practice"
        self.ensure_root()

    def ensure_root(self):
        if not self.practice_root.exists():
            self.practice_root.mkdir(parents=True)

    def sanitize_name(self, name):
        """Turn 'Hello World!' into 'Hello_World'"""
        return re.sub(r'[^a-zA-Z0-9]', '_', name).strip('_')

    def scaffold_exercise(self, exercise):
        """
        Takes an exercise dict from DB and creates the folder structure.
        exercise: {
            'day_number': 1,
            'difficulty': 'Easy',
            'title': 'Hello World',
            'starter_code': '...',
            'test_code': '...',
            'solution_code': '...',
            'instructions': '...'
        }
        """
        day = exercise.get('day_number', 0)
        diff = exercise.get('difficulty', 'Unknown')
        title = self.sanitize_name(exercise.get('title', 'Untitled'))
        
        # Path: ~/PyNexus_Practice/Day_01/Easy_Hello_World
        day_dir = self.practice_root / f"Day_{day:02d}"
        ex_dir = day_dir / f"{diff}_{title}"
        
        if not ex_dir.exists():
            ex_dir.mkdir(parents=True)
            
        # 1. Write README.md (Instructions)
        readme = ex_dir / "README.md"
        instructions = f"# {exercise.get('title')}\n\n"
        instructions += f"**Difficulty:** {diff}\n"
        instructions += f"**Day:** {day}\n\n"
        instructions += "## Instructions\n"
        instructions += exercise.get('instructions', "No instructions provided.")
        readme.write_text(instructions, encoding='utf-8')
        
        # 2. Write main.py (Starter Code)
        # Only write if invalid/empty to allow user progress persistence
        main_py = ex_dir / "main.py"
        starter = exercise.get('starter_code', '')
        if not main_py.exists():
             main_py.write_text(starter, encoding='utf-8')
             
        # 3. Write test_main.py (Hidden Tests)
        # Always overwrite tests to prevent cheating/modification
        test_py = ex_dir / "test_main.py"
        test_content = exercise.get('test_code', '')
        
        # If test_code doesn't have a proper pytest function, wrap it
        if test_content and 'def test_' not in test_content:
            # It's a raw script - wrap in pytest function
            wrapped_test = '''import main
import sys
from io import StringIO

def test_solution(capsys):
    """Auto-generated pytest wrapper for raw test script."""
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        # Re-import main to re-execute
        import importlib
        importlib.reload(main)
        output = sys.stdout.getvalue().strip()
    finally:
        sys.stdout = old_stdout
    
    # Original test assertion
'''
            # Extract the assertion from raw test if present
            if 'assert' in test_content:
                # Find the assert statement
                import re
                match = re.search(r"assert\s+(.+)", test_content)
                if match:
                    assertion = match.group(0)
                    # Convert to use 'output' variable
                    assertion = assertion.replace('captured.out.strip()', 'output')
                    assertion = assertion.replace('output.strip()', 'output')
                    wrapped_test += f"    {assertion}\n"
                else:
                    wrapped_test += f"    assert output != ''\n"
            else:
                # No assert found, just check it runs
                wrapped_test += "    assert True  # Test ran successfully\n"
            
            test_content = wrapped_test
        
        test_py.write_text(test_content, encoding='utf-8')
        
        return ex_dir

    def launch_vscode(self, path):
        """Opens VS Code at the specific path."""
        try:
            # Code is usually in PATH.
            # Windows: 'code.cmd' or 'code'
            cmd = "code"
            if os.name == 'nt':
                cmd = "code.cmd" # Sometimes safer on Windows
                
            # Fallback to just 'code' if cmd check fails logic, 
            # but subprocess allows 'code' usually.
            subprocess.Popen(["code", str(path)], shell=True)
            return True, f"Launched VS Code at {path}"
        except Exception as e:
            return False, f"Failed to launch VS Code: {e}"
    
    def get_exercise_path(self, exercise) -> Path:
        """Get the path where an exercise would be scaffolded."""
        day = exercise.get('day_number', 0)
        diff = exercise.get('difficulty', 'Unknown')
        title = self.sanitize_name(exercise.get('title', 'Untitled'))
        return self.practice_root / f"Day_{day:02d}" / f"{diff}_{title}"
    
    def run_tests(self, exercise_path):
        """
        Run pytest on the exercise and return results.
        Returns: (passed: bool, output: str, stats: dict)
        """
        test_file = Path(exercise_path) / "test_main.py"
        
        if not test_file.exists():
            return False, "Test file not found!", {"passed": 0, "failed": 1, "error": True}
        
        try:
            result = subprocess.run(
                ["pytest", str(test_file), "-v", "--tb=short"],
                cwd=str(exercise_path),
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            output = result.stdout + result.stderr
            passed = result.returncode == 0
            
            # Parse basic stats from output
            stats = {"passed": 0, "failed": 0, "error": False}
            if "passed" in output:
                import re
                match = re.search(r'(\d+) passed', output)
                if match:
                    stats["passed"] = int(match.group(1))
            if "failed" in output:
                import re
                match = re.search(r'(\d+) failed', output)
                if match:
                    stats["failed"] = int(match.group(1))
            
            return passed, output, stats
            
        except subprocess.TimeoutExpired:
            return False, "⏱️ Test timed out after 30 seconds!", {"passed": 0, "failed": 0, "error": True}
        except FileNotFoundError:
            return False, "❌ pytest not found! Please install: pip install pytest", {"passed": 0, "failed": 0, "error": True}
        except Exception as e:
            return False, f"❌ Error running tests: {e}", {"passed": 0, "failed": 0, "error": True}

