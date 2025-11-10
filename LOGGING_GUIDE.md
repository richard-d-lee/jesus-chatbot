# Chat Logging System Documentation

## Overview

The Jesus Chatbot now includes a comprehensive logging system that tracks all user interactions with the following features:

- **User Questions & Answers**: Records every conversation
- **Location Tracking**: Captures user location based on IP address (country, region, city, coordinates)
- **Automatic Cleanup**: Automatically deletes logs older than 7 days
- **Admin Dashboard**: API endpoints to view and analyze chat logs

## Features

### 1. Automatic Logging

Every chat interaction is automatically logged with the following information:

- User's question
- Bot's response
- Jesus representation used (traditional, historical, african, mormon, ai, current)
- Scripture mode settings (enabled/disabled, Bible version)
- User's IP address
- Geographic location (country, region, city, latitude, longitude)
- Response source (OpenAI API or fallback)
- Timestamp

### 2. Location Tracking

The system uses the free **ip-api.com** service to determine user location from their IP address. This provides:

- Country
- Region/State
- City
- Latitude/Longitude coordinates

**Note**: For local development (127.0.0.1 or 192.168.x.x), location is recorded as "Local".

### 3. Automatic Cleanup

Logs are automatically deleted after **7 days** to comply with privacy best practices and reduce database size.

- **Automatic Daily Cleanup**: Runs every day at midnight UTC
- **Manual Cleanup**: Can be triggered via API endpoint

## API Endpoints

### View Chat Logs

**GET** `/api/admin/logs`

Retrieve chat logs with optional filtering.

**Query Parameters:**
- `period`: `week` (default) or `all`
- `limit`: Number of logs to return (default: 100)

**Example:**
```bash
curl http://localhost:5000/api/admin/logs?period=week&limit=50
```

**Response:**
```json
{
  "success": true,
  "count": 25,
  "logs": [
    {
      "id": 1,
      "user_id": null,
      "representation": "current",
      "user_message": "What is the meaning of life?",
      "bot_response": "The meaning of life is to love God...",
      "scripture_mode": true,
      "bible_version": "NIV",
      "ip_address": "203.0.113.45",
      "country": "United States",
      "region": "California",
      "city": "San Francisco",
      "latitude": 37.7749,
      "longitude": -122.4194,
      "response_source": "openai",
      "created_at": "2025-11-10T12:34:56"
    }
  ]
}
```

### View Statistics

**GET** `/api/admin/logs/stats`

Get aggregated statistics for the past week.

**Example:**
```bash
curl http://localhost:5000/api/admin/logs/stats
```

**Response:**
```json
{
  "success": true,
  "period": "past_week",
  "stats": {
    "total_chats": 150,
    "scripture_mode_usage": 45,
    "by_representation": {
      "current": 60,
      "traditional": 40,
      "historical": 25,
      "african": 15,
      "ai": 8,
      "mormon": 2
    },
    "by_country": {
      "United States": 100,
      "United Kingdom": 25,
      "Canada": 15,
      "Australia": 10
    }
  }
}
```

### Manual Cleanup

**POST** `/api/admin/logs/cleanup`

Manually trigger deletion of logs older than 7 days.

**Example:**
```bash
curl -X POST http://localhost:5000/api/admin/logs/cleanup
```

**Response:**
```json
{
  "success": true,
  "message": "Deleted 23 old log entries",
  "deleted_count": 23
}
```

## Database Schema

### ChatLog Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User table (nullable for anonymous users) |
| representation | String(50) | Which Jesus representation was used |
| user_message | Text | The user's question |
| bot_response | Text | Jesus's answer |
| scripture_mode | Boolean | Whether scripture mode was enabled |
| bible_version | String(10) | Bible version used (KJV, NIV, ESV, NRSV) |
| ip_address | String(45) | User's IP address (IPv4 or IPv6) |
| country | String(100) | User's country |
| region | String(100) | User's region/state |
| city | String(100) | User's city |
| latitude | Float | Geographic latitude |
| longitude | Float | Geographic longitude |
| response_source | String(20) | 'openai' or 'fallback' |
| created_at | DateTime | Timestamp of the conversation |

## Files Added/Modified

### New Files

1. **`src/models/chat_log.py`** - ChatLog database model
2. **`src/utils/geolocation.py`** - IP geolocation utilities
3. **`src/routes/admin.py`** - Admin API endpoints for viewing logs
4. **`src/utils/scheduler.py`** - Automatic cleanup scheduler
5. **`LOGGING_GUIDE.md`** - This documentation file

### Modified Files

1. **`src/main.py`** - Added admin blueprint and scheduler initialization
2. **`src/routes/chatbot.py`** - Added logging to all chat endpoints

## Privacy & Security Considerations

### Data Retention

- Logs are automatically deleted after **7 days**
- This complies with privacy best practices for temporary logging
- Adjust retention period by modifying the `timedelta(days=7)` in `src/models/chat_log.py`

### IP Address Storage

- IP addresses are stored for geolocation purposes
- Consider anonymizing IPs in production (e.g., masking last octet)
- Comply with GDPR, CCPA, and other privacy regulations in your jurisdiction

### Geolocation Service

- Currently uses **ip-api.com** free tier (45 requests/minute)
- For high-traffic production use, consider:
  - Upgrading to ip-api.com Pro
  - Using alternative services (MaxMind GeoIP2, IPinfo, etc.)
  - Implementing rate limiting and caching

### Admin Access

**IMPORTANT**: The admin endpoints are currently **unprotected**. Before deploying to production:

1. Add authentication to admin routes
2. Implement role-based access control
3. Use environment variables for admin credentials

**Example Protection** (add to `src/routes/admin.py`):

```python
from functools import wraps
from flask import request, jsonify
import os

def require_admin_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-Admin-Key')
        if api_key != os.environ.get('ADMIN_API_KEY'):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Then add @require_admin_key decorator to each endpoint
@admin_bp.route('/logs', methods=['GET'])
@require_admin_key
def get_logs():
    # ... existing code
```

## Usage Examples

### View Recent Logs

```bash
# Get last 100 logs from past week
curl http://localhost:5000/api/admin/logs

# Get all logs
curl http://localhost:5000/api/admin/logs?period=all

# Get last 10 logs
curl http://localhost:5000/api/admin/logs?limit=10
```

### Analyze Usage Patterns

```bash
# Get statistics
curl http://localhost:5000/api/admin/logs/stats | jq .
```

### Clean Up Old Logs

```bash
# Manually trigger cleanup
curl -X POST http://localhost:5000/api/admin/logs/cleanup
```

## Testing

A test script is included to verify the logging system:

```bash
python3 test_logging.py
```

This will:
- Create test database tables
- Insert sample log entries
- Test retrieval functions
- Test automatic deletion
- Verify all functionality works correctly

## Deployment Notes

### Environment Variables

No additional environment variables are required. The logging system uses the existing database configuration.

### Database Migration

When deploying to production, the new `chat_logs` table will be automatically created on first run.

For existing deployments:
1. The system will automatically create the new table
2. No manual migration is needed
3. Existing data is not affected

### Performance Considerations

- Geolocation API calls add ~100-300ms latency per chat
- Consider implementing caching for repeated IP addresses
- Monitor database size if traffic is high
- Adjust cleanup frequency if needed

## Monitoring

### Check Scheduler Status

The scheduler logs to console:
```
[SCHEDULER] Log cleanup scheduler started
[SCHEDULER] Next cleanup scheduled in 12.5 hours
[SCHEDULER] Automatic cleanup completed: 45 old logs deleted
```

### Database Size

Monitor the `chat_logs` table size:
```sql
SELECT COUNT(*) FROM chat_logs;
SELECT COUNT(*) FROM chat_logs WHERE created_at >= datetime('now', '-7 days');
```

## Troubleshooting

### Geolocation Not Working

If location data is not being captured:
1. Check internet connectivity
2. Verify ip-api.com is accessible
3. Check rate limits (45 requests/minute on free tier)
4. Review console logs for errors

### Logs Not Being Deleted

If automatic cleanup isn't working:
1. Check scheduler logs in console
2. Verify scheduler started: `[SCHEDULER] Log cleanup scheduler started`
3. Manually trigger cleanup: `POST /api/admin/logs/cleanup`

### Database Errors

If you encounter database errors:
1. Delete the database file and restart (development only)
2. Check file permissions on database directory
3. Verify SQLAlchemy is properly installed

## Future Enhancements

Consider adding:
- Admin web dashboard for viewing logs
- Export logs to CSV/JSON
- Real-time analytics
- User-specific log viewing (for authenticated users)
- Advanced filtering (by date range, representation, location)
- Anonymization options for privacy compliance
- Rate limiting per IP address
- Abuse detection and blocking

## Support

For questions or issues with the logging system, please refer to the main project documentation or create an issue on GitHub.
