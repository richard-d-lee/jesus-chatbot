# Jesus Christ Chatbot

A spiritual AI companion featuring six distinct representations of Jesus Christ, powered by OpenAI's GPT-4.

## Features

- **6 Jesus Representations**:
  - Traditional Western Jesus
  - Historical Middle Eastern Jesus
  - African Diaspora Jesus
  - Mormon Jesus (Book of Mormon tradition)
  - AI Jesus (digital consciousness)
  - Current Jesus (walking among us today)

- **Scripture Mode**: Get responses with Bible verses from KJV, NIV, ESV, or NRSV
- **Conversation History**: Save and load your spiritual conversations
- **User Authentication**: Optional login to persist conversations across devices
- **Mobile Responsive**: Beautiful interface on all screen sizes
- **Buy Me a Coffee Integration**: Support the project at [buymeacoffee.com/jesusexpress](https://buymeacoffee.com/jesusexpress)

## Quick Start

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete deployment instructions.

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

3. Run the application:
```bash
python src/main.py
```

4. Open http://localhost:5000 in your browser

## Deployment

This application is ready to deploy to:
- **Render** (recommended) - See deployment guide
- **Railway** - See deployment guide
- **Heroku** - Use included Procfile

## Technology Stack

- **Backend**: Flask (Python)
- **AI**: OpenAI GPT-4
- **Database**: SQLite (default) or PostgreSQL
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Authentication**: Flask-Login with SQLAlchemy

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `SECRET_KEY` | Flask session secret | No (auto-generated) |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `PORT` | Server port | No (defaults to 5000) |

## License

Free to use for spiritual and educational purposes.

## Support

Donations help keep this tool free and accessible: [buymeacoffee.com/jesusexpress](https://buymeacoffee.com/jesusexpress)

---

*"For where two or three gather in my name, there am I with them." - Matthew 18:20*
