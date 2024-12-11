import asyncio
import logging
import time
import tweepy
from datetime import datetime
from config import *
from scheduler import PostScheduler
from content_generator import ContentGenerator

class PostPublisher:
    def __init__(self):
        self.scheduler = PostScheduler()
        self.generator = ContentGenerator()
        self.logger = logging.getLogger('PostPublisher')
        
        self.twitter_client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )

    def publish_post(self, content=None):
        """Publish a post to Twitter"""
        try:
            if not content:
                content = self.generator.generate_post()
            if content:
                response = self.twitter_client.create_tweet(text=content)
                self.logger.info(f"Published tweet: {response.data['id']}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error publishing tweet: {e}")
            return False

    def run(self):
        """Main execution loop"""
        while True:
            try:
                if self.scheduler.needs_new_schedule():
                    self.scheduler.generate_new_schedule()

                next_post_time = self.scheduler.get_next_post_time()
                if not next_post_time:
                    continue

                now = datetime.now(DEFAULT_TIMEZONE)
                if now >= next_post_time:
                    if self.publish_post():
                        self.scheduler.remove_posted_time(next_post_time)
                    
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                time.sleep(300)  # Wait 5 minutes on error