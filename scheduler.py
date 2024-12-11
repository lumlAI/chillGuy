import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
import logging
from config import *

class PostScheduler:
   def __init__(self):
       self.current_schedule = self._load_schedule()
       self.logger = logging.getLogger('PostScheduler')

   def _load_schedule(self) -> Dict:
       """Load existing schedule from file"""
       try:
           with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
               return json.load(f)
       except FileNotFoundError:
           return {"posts": [], "last_post_time": None}
   def _load_schedule(self) -> Dict:
    """Load existing schedule from file"""
    try:
        with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
           return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
       # Create initial schedule if file doesn't exist or is invalid
       initial_schedule = {"posts": [], "last_post_time": None}
       with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
           json.dump(initial_schedule, f, indent=4)
       return initial_schedule
   def _save_schedule(self) -> None:
       """Save current schedule to file"""
       with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
           json.dump(self.current_schedule, f, indent=4)

   def generate_new_schedule(self) -> List[datetime]:
       """Generate new posting schedule"""
       now = datetime.now(DEFAULT_TIMEZONE)
       
       # Get last post time from previous schedule
       last_post_time = None
       if self.current_schedule["last_post_time"]:
           last_post_time = datetime.fromisoformat(self.current_schedule["last_post_time"])

       # Ensure minimum gap between schedules
       start_time = now
       if last_post_time:
           min_start_time = last_post_time + timedelta(minutes=MIN_SCHEDULE_GAP_MINUTES)
           start_time = max(now, min_start_time)

       # Generate new schedule
       post_count = random.randint(MIN_POSTS_PER_SCHEDULE, MAX_POSTS_PER_SCHEDULE)
       post_times = []
       current_time = start_time

       for _ in range(post_count):
           interval = random.randint(MIN_INTERVAL_MINUTES, MAX_INTERVAL_MINUTES)
           if post_times:
               current_time = post_times[-1] + timedelta(minutes=interval)
           post_times.append(current_time)

       # Update schedule
       self.current_schedule = {
           "posts": [time.isoformat() for time in post_times],
           "last_post_time": post_times[-1].isoformat()
       }
       self._save_schedule()
       
       self.logger.info(f"Generated new schedule with {post_count} posts")
       return post_times

   def get_next_post_time(self) -> datetime:
       """Get next scheduled post time"""
       now = datetime.now(DEFAULT_TIMEZONE)
       
       for post_time in self.current_schedule["posts"]:
           scheduled_time = datetime.fromisoformat(post_time)
           if scheduled_time > now:
               return scheduled_time
               
       return None

   def remove_posted_time(self, post_time: datetime) -> None:
       """Remove a post time after publishing"""
       self.current_schedule["posts"] = [
           pt for pt in self.current_schedule["posts"] 
           if datetime.fromisoformat(pt) != post_time
       ]
       self._save_schedule()

   def needs_new_schedule(self) -> bool:
       """Check if new schedule needs to be generated"""
       return len(self.current_schedule["posts"]) == 0