 Overview
Automated system for scheduling and publishing Twitter posts using AI-generated content.

## System Architecture
- `config.py`: Configuration and environment variables
- `scheduler.py`: Post scheduling management
- `content_generator.py`: AI content generation
- `publisher.py`: Twitter publishing interface
- `main.py`: Entry point and CLI handling

## Key Components

### Configuration (config.py)
```python
MIN_POSTS_PER_SCHEDULE = 3
MAX_POSTS_PER_SCHEDULE = 7
MIN_INTERVAL_MINUTES = 30
MAX_INTERVAL_MINUTES = 180
```

### Scheduler
- Manages posting schedules
- Stores schedule in JSON format
- Ensures minimum gaps between posts
- Auto-generates new schedules when needed

### Content Generator
- Integrates with Mistral AI
- Uses predefined topics from topics.txt
- Enforces Twitter's 280-character limit
- Handles content generation errors

### Publisher
- Twitter API integration via tweepy
- Automated posting based on schedule
- Manual posting via CLI command
- Error handling and logging

## File Structure
```
project/
├── data/
│   ├── topics.txt    # Post topics
│   └── schedule.json # Schedule state
├── logs/
│   └── posting_service.log
└── src/
    ├── config.py
    ├── scheduler.py
    ├── content_generator.py
    ├── publisher.py
    └── main.py
```

## Usage

### Automated Mode
```bash
python main.py
```

### Manual Post
```bash
python main.py /post
```

## Dependencies
```
mistralai>=0.0.7
tweepy>=4.14.0
pytz>=2023.3
python-dotenv>=1.0.0
```

## Environment Variables
Required API keys:
```
MISTRAL_API_KEY
AGENT_ID
TWITTER_API_KEY
TWITTER_API_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET
```

## Error Handling
- File system errors
- API failures
- Content generation issues
- Twitter posting limits

## Logging
All actions logged to `logs/posting_service.log`:
- Schedule generation
- Post creation
- Publishing status
- Errors

## Scheduling Logic
1. Generate 3-7 posts per schedule
2. Intervals: 30-180 minutes between posts
3. Minimum 60-minute gap between schedules
4. Auto-regenerates when schedule depleted

## Security Considerations
- API keys stored as environment variables
- Rate limiting compliance
- Error recovery mechanisms

## Maintenance
Regular checks required for:
- API key validity
- Log file size
- Schedule.json integrity
- Topics.txt updates