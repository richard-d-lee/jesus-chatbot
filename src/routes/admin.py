from flask import Blueprint, jsonify, request
from src.models.chat_log import ChatLog
from src.models.user import db
from datetime import datetime, timedelta
from functools import wraps
import os

admin_bp = Blueprint('admin', __name__)

def require_admin_key(f):
    """
    Decorator to require API key authentication for admin endpoints.
    API key should be passed in the X-Admin-Key header.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from header
        provided_key = request.headers.get('X-Admin-Key')
        
        # Get expected key from environment variable
        expected_key = os.environ.get('ADMIN_API_KEY')
        
        # If no key is set in environment, deny access
        if not expected_key:
            return jsonify({
                'success': False,
                'message': 'Admin API is not configured. Please set ADMIN_API_KEY environment variable.'
            }), 500
        
        # Check if provided key matches
        if not provided_key or provided_key != expected_key:
            return jsonify({
                'success': False,
                'message': 'Unauthorized. Please provide valid X-Admin-Key header.'
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/logs', methods=['GET'])
@require_admin_key
def get_logs():
    """
    Get chat logs with optional filtering.
    Query parameters:
    - period: 'week' (default), 'all'
    - limit: number of logs to return (default: 100)
    """
    try:
        period = request.args.get('period', 'week')
        limit = request.args.get('limit', 100, type=int)
        
        if period == 'week':
            logs = ChatLog.get_logs_past_week()
        else:
            logs = ChatLog.get_all_logs()
        
        # Apply limit
        logs = logs[:limit] if limit else logs
        
        return jsonify({
            'success': True,
            'count': len(logs),
            'logs': [log.to_dict() for log in logs]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@admin_bp.route('/logs/stats', methods=['GET'])
@require_admin_key
def get_log_stats():
    """
    Get statistics about chat logs for the past week.
    """
    try:
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        
        # Total chats in past week
        total_chats = ChatLog.query.filter(ChatLog.created_at >= one_week_ago).count()
        
        # Chats by representation
        from sqlalchemy import func
        representation_stats = db.session.query(
            ChatLog.representation,
            func.count(ChatLog.id).label('count')
        ).filter(
            ChatLog.created_at >= one_week_ago
        ).group_by(ChatLog.representation).all()
        
        # Chats by country
        country_stats = db.session.query(
            ChatLog.country,
            func.count(ChatLog.id).label('count')
        ).filter(
            ChatLog.created_at >= one_week_ago,
            ChatLog.country.isnot(None)
        ).group_by(ChatLog.country).all()
        
        # Scripture mode usage
        scripture_count = ChatLog.query.filter(
            ChatLog.created_at >= one_week_ago,
            ChatLog.scripture_mode == True
        ).count()
        
        return jsonify({
            'success': True,
            'period': 'past_week',
            'stats': {
                'total_chats': total_chats,
                'scripture_mode_usage': scripture_count,
                'by_representation': {rep: count for rep, count in representation_stats},
                'by_country': {country: count for country, count in country_stats}
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@admin_bp.route('/logs/cleanup', methods=['POST'])
@require_admin_key
def cleanup_old_logs():
    """
    Manually trigger cleanup of logs older than 7 days.
    This is also run automatically, but can be triggered manually.
    """
    try:
        deleted_count = ChatLog.delete_old_logs()
        
        return jsonify({
            'success': True,
            'message': f'Deleted {deleted_count} old log entries',
            'deleted_count': deleted_count
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
