import logging
import sys
from config import LOG_FILE
from publisher import PostPublisher
from content_generator import ContentGenerator

def setup_logging():
   logging.basicConfig(
       filename=LOG_FILE,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       level=logging.INFO
   )

def handle_post_command():
   setup_logging()
   generator = ContentGenerator()
   publisher = PostPublisher()
   content = generator.generate_post()
   if content:
       success = publisher.publish_post(content)
       if success:
           print("Post successfully published!")
           return True
   print("Failed to publish post")
   return False

def main():
   setup_logging()
   if len(sys.argv) > 1 and sys.argv[1] == '/post':
       handle_post_command()
       return

   publisher = PostPublisher()
   try:
       publisher.run()
   except KeyboardInterrupt:
       print("\nShutting down gracefully...")
   except Exception as e:
       logging.error(f"Error in main loop: {e}")

if __name__ == '__main__':
   main()