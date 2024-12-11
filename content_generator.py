import random
import logging
from mistralai import Mistral
from config import *

class ContentGenerator:
   def __init__(self):
       self.client = Mistral(api_key=MISTRAL_API_KEY)
       self.logger = logging.getLogger('ContentGenerator')
       self.topics = self._load_topics()

   def _load_topics(self) -> list:
       try:
           with open(TOPICS_FILE, 'r') as f:
               return [line.strip() for line in f if line.strip()]
       except FileNotFoundError:
           self.logger.error(f"Topics file not found: {TOPICS_FILE}")
           return []

   def get_random_topic(self) -> str:
       return random.choice(self.topics) if self.topics else "General discussion topic"

   def generate_post(self) -> str:
       topic = self.get_random_topic()
       prompt = f"Create an engaging social media post about: {topic}"
       
       try:
           response = self.client.agents.complete(
               agent_id=AGENT_ID,
               messages=[{"role": "user", "content": prompt}]
           )
           content = response.choices[0].message.content
           
           if len(content) > 280:
               content = content[:277] + "..."
           
           self.logger.info(f"Generated post about topic: {topic}")
           return content
           
       except Exception as e:
           self.logger.error(f"Error generating content: {e}")
           return None