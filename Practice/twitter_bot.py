import tweepy
import os

# --- Configuration ---
# You will get these from the Twitter Developer Portal
# Do not commit these keys into GitHub or share them publicly!
API_KEY = "YOUR_API_KEY_HERE"
API_KEY_SECRET = "YOUR_API_KEY_SECRET_HERE"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET_HERE"


def authenticate_twitter():
    """Authenticates to the Twitter/X API using OAuth 1.0a."""
    try:
        # Note: In the Free tier (API v2), you need to use the Client class
        # for creating tweets, not the older OAuth1UserHandler/API class.
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        print("✅ Successfully authenticated with Twitter/X!")
        return client
    except Exception as e:
        print(f"❌ Error authenticating: {e}")
        return None


def post_learning_update(client, day, topic, concepts):
    """Posts a status update to Twitter/X."""
    if not client:
        print("Cannot post without authentication.")
        return

    # Create the tweet content
    tweet_text = (
        f"🚀 Python Learning Journey - Day {day}!\n\n"
        f"Today I learned about: {topic}\n"
        f"Key concepts: {concepts}\n\n"
        f"#Python #CodingJourney #LearnToCode"
    )

    try:
        # Use the v2 API to create a tweet
        response = client.create_tweet(text=tweet_text)
        print(f"✅ Successfully tweeted!")
        print(f"Tweet ID: {response.data['id']}")
        
    except tweepy.errors.Forbidden as e:
         print(f"❌ Forbidden Error (403). This usually means your app does not have Write permissions.")
         print("Go to Developer Portal -> Projects & Apps -> Your App -> User authentication settings")
         print("Ensure 'Read and write' is selected under App permissions.")
         print(f"Error Details: {e}")
    except Exception as e:
        print(f"❌ Error posting tweet: {e}")


if __name__ == "__main__":
    # --- Example Usage ---
    # 1. Authenticate
    twitter_client = authenticate_twitter()

    # 2. To test this later, uncomment the lines below and fill in the details!
    """
    if twitter_client:
        day_number = 5
        topic_learned = "While and For Loops"
        key_concepts = "Iterating over lists, infinite loops, break/continue statements."
        post_learning_update(twitter_client, day_number, topic_learned, key_concepts)
    """
    
    # Just a placeholder for now to let you know the script ran.
    if twitter_client and API_KEY == "YOUR_API_KEY_HERE":
       print("⚠️ Warning: You need to replace the placeholder keys at the top of the file!")

