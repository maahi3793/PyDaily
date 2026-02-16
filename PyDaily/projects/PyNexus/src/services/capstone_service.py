"""
Capstone Service - Fetches Capstone projects and stories from Supabase.
"""
from services.auth import AuthService


class CapstoneService:
    """Service for fetching Capstone project data."""
    
    def __init__(self):
        self.auth = AuthService()
        self.client = self.auth.client
    
    def get_projects(self):
        """Get all capstone projects."""
        try:
            response = self.client.table("capstone_projects").select("*").order("phase").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching capstone projects: {e}")
            return []
    
    def get_project_for_phase(self, phase: int):
        """Get the capstone project for a specific phase."""
        try:
            response = self.client.table("capstone_projects").select("*").eq("phase", phase).limit(1).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching project for phase {phase}: {e}")
            return None
    
    def get_stories_for_project(self, project_id: str):
        """Get all stories for a specific project, ordered by order_num."""
        try:
            response = self.client.table("capstone_stories").select("*").eq("project_id", project_id).order("order_num").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching stories for project {project_id}: {e}")
            return []
    
    def get_stories_for_phase(self, phase: int):
        """Convenience method: get project and stories for a phase in one call."""
        project = self.get_project_for_phase(phase)
        if not project:
            return None, []
        stories = self.get_stories_for_project(project['id'])
        return project, stories
