# Deployment Guide for Jesus Christ AI Chatbot

## Quick Deployment with Manus

### Backend Deployment (Recommended)
```bash
# Deploy the entire application (backend + frontend)
service_deploy_backend flask /path/to/jesus-chatbot-package
```

This will:
- Deploy the Flask backend with all API endpoints
- Serve the frontend files from the static folder
- Provide a permanent public URL
- Handle CORS and routing automatically

### Frontend-Only Deployment
```bash
# Deploy just the frontend (requires separate backend)
service_deploy_frontend static /path/to/jesus-chatbot-package/src/static
```

## Manual Deployment

### Local Development
```bash
cd jesus-chatbot-package
pip install -r requirements.txt
python src/main.py
```
Access at: http://localhost:5000

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "src/main.py"]
```

## Environment Variables

### Required for Production
```bash
export FLASK_ENV=production
export SECRET_KEY="your-secret-key-here"
```

### Optional
```bash
export OPENAI_API_KEY="your-openai-key"  # For default API access
export DATABASE_URL="sqlite:///app.db"   # Custom database location
```

## Database Setup

The application automatically creates SQLite database tables on first run. For production, consider using PostgreSQL:

```python
# In src/main.py, replace:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
```

## Security Considerations

1. **Secret Key**: Use a strong, random secret key in production
2. **HTTPS**: Deploy behind HTTPS proxy (nginx, cloudflare)
3. **API Keys**: Users should provide their own OpenAI keys
4. **Rate Limiting**: Consider adding rate limiting for API endpoints
5. **Input Validation**: All user inputs are validated on backend

## Monitoring

### Health Check Endpoint
Add to `src/main.py`:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure CORS is enabled in main.py
2. **Database Errors**: Check file permissions for SQLite
3. **API Timeouts**: Verify OpenAI API key configuration
4. **Static Files**: Ensure static folder path is correct

### Debug Mode
```bash
export FLASK_DEBUG=1
python src/main.py
```

## Performance Optimization

1. **Static Files**: Use CDN for images in production
2. **Database**: Add indexes for frequently queried fields
3. **Caching**: Implement Redis for session storage
4. **Load Balancing**: Use multiple Gunicorn workers

## Backup Strategy

### Database Backup
```bash
# SQLite backup
cp src/database/app.db backup/app_$(date +%Y%m%d).db

# PostgreSQL backup
pg_dump dbname > backup/db_$(date +%Y%m%d).sql
```

### Full Application Backup
```bash
tar -czf jesus-chatbot-backup-$(date +%Y%m%d).tar.gz jesus-chatbot-package/
```

## Scaling Considerations

For high traffic:
1. Use PostgreSQL instead of SQLite
2. Implement Redis for session management
3. Add load balancer (nginx)
4. Use separate API key management service
5. Implement conversation caching
6. Add CDN for static assets

## Support

For deployment issues:
1. Check application logs
2. Verify all dependencies are installed
3. Ensure proper file permissions
4. Test API endpoints individually
5. Verify database connectivity

