import os
from datetime import datetime, timedelta
import pytz

# API Keys and Constants
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
AGENT_ID = os.getenv('AGENT_ID')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Timezone settings
DEFAULT_TIMEZONE = pytz.timezone('UTC')

# Schedule settings
MIN_POSTS_PER_SCHEDULE = 3
MAX_POSTS_PER_SCHEDULE = 7
MIN_INTERVAL_MINUTES = 30
MAX_INTERVAL_MINUTES = 180
MIN_SCHEDULE_GAP_MINUTES = 60  # Minimum gap between schedules

# File paths
TOPICS_FILE = 'data/topics.txt'
SCHEDULE_FILE = 'data/schedule.json'
LOG_FILE = 'logs/posting_service.log'