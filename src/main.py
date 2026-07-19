import os
import sys
import secrets
import logging
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from src.models.user import db
from src.models.chat_log import ChatLog
from src.models.user_location import UserLocation
from src.routes.user import user_bp
from src.routes.chatbot import chatbot_bp
from src.routes.auth import auth_bp
from src.routes.admin import admin_bp
from src.utils.scheduler import LogCleanupScheduler
from src.utils.limiter import limiter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# SECRET_KEY must be stable across restarts/workers or all sessions break.
secret_key = os.environ.get('SECRET_KEY')
if not secret_key:
    secret_key = secrets.token_hex(32)
    logger.warning("SECRET_KEY env var not set - using a random key; sessions will not survive restarts")
app.config['SECRET_KEY'] = secret_key

# Trust exactly one proxy hop (Render/Railway) so request.remote_addr is the
# real client IP and can't be spoofed via X-Forwarded-For.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# CORS is only needed for the admin dashboards, which are opened as local
# files. Everything else is same-origin.
CORS(app, resources={r"/api/admin/*": {
    "origins": "*",
    "allow_headers": ["Content-Type", "X-Admin-Key"]
}})

limiter.init_app(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Database: use DATABASE_URL (Postgres) when provided, SQLite for local dev.
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # SQLAlchemy requires the postgresql:// scheme; Render supplies postgres://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    logger.info("Using Postgres database")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    logger.warning("DATABASE_URL not set - using local SQLite (data will NOT survive redeploys on ephemeral hosts)")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Long-lived caching for images; CSS/JS use ?v= cache busting in the HTML.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

scheduler = LogCleanupScheduler(app)
scheduler.start()

@app.after_request
def set_cache_headers(response):
    # HTML must always revalidate so deploys show up immediately.
    if response.mimetype == 'text/html':
        response.headers['Cache-Control'] = 'no-cache'
    return response

# SEO Routes - Explicit routes for better SEO
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml', mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt', mimetype='text/plain')

@app.route('/contact')
def contact():
    return send_from_directory(app.static_folder, 'contact.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
