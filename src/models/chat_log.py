from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from src.models.user import db

class ChatLog(db.Model):
    """Model for tracking all chat interactions with user location data"""
    __tablename__ = 'chat_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # User information (nullable for anonymous users)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Chat details
    representation = db.Column(db.String(50), nullable=False)  # which Jesus representation
    user_message = db.Column(db.Text, nullable=False)  # user's question
    bot_response = db.Column(db.Text, nullable=False)  # Jesus's answer
    
    # Scripture mode settings
    scripture_mode = db.Column(db.Boolean, default=False)
    bible_version = db.Column(db.String(10), nullable=True)  # kjv, niv, esv, nrsv
    
    # Location data
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6
    country = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Metadata
    response_source = db.Column(db.String(20), nullable=True)  # 'openai' or 'fallback'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert log entry to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'representation': self.representation,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'scripture_mode': self.scripture_mode,
            'bible_version': self.bible_version,
            'ip_address': self.ip_address,
            'country': self.country,
            'region': self.region,
            'city': self.city,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'response_source': self.response_source,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def get_logs_past_week(cls):
        """Get all logs from the past 7 days"""
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        return cls.query.filter(cls.created_at >= one_week_ago).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def delete_old_logs(cls):
        """Delete logs older than 7 days"""
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        deleted_count = cls.query.filter(cls.created_at < one_week_ago).delete()
        db.session.commit()
        return deleted_count
    
    @classmethod
    def get_all_logs(cls):
        """Get all logs (for admin view)"""
        return cls.query.order_by(cls.created_at.desc()).all()
