import requests
import json
import logging

class LinkedInService:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0" # Required for modern APIs
        }
        self.user_urn = None

    def get_user_urn(self):
        """
        Fetches the authenticated user's URN (ID).
        This is needed to post 'as' this user.
        """
        if self.user_urn:
            return self.user_urn

        try:
            # The 'me' endpoint returns basic profile info
            response = requests.get(f"{self.base_url}/me", headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                # URN format: 'urn:li:person:ID'
                self.user_urn = f"urn:li:person:{data['id']}"
                logging.info(f"LinkedIn Auth Successful. User URN: {self.user_urn}")
                return self.user_urn
            else:
                logging.error(f"Failed to fetch LinkedIn Profile: {response.text}")
                return None
        except Exception as e:
            logging.error(f"LinkedIn Init Error: {e}")
            return None

    def post_update(self, text):
        """
        Posts a simple text update (UGC Post) to the user's feed.
        """
        if not self.access_token:
            logging.warning("LinkedIn Token missing. Skipping post.")
            return False

        urn = self.get_user_urn()
        if not urn:
            logging.error("Cannot post to LinkedIn: User URN not found.")
            return False

        # Endpoint: ugcPosts (User Generated Content)
        url = f"{self.base_url}/ugcPosts"
        
        # Payload Structure for Text Post
        payload = {
            "author": urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 201:
                logging.info("✅ LinkedIn Post Published Successfully!")
                return True
            else:
                logging.error(f"❌ LinkedIn Post Failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"LinkedIn Network Error: {e}")
            return False
