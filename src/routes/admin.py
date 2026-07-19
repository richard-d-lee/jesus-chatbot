import os
import logging
from functools import wraps
from flask import Blueprint, jsonify, request
from src.models.chat_log import ChatLog
from src.models.user import db
from src.models.user_location import UserLocation
from src.utils.limiter import limiter
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)
logger = logging.getLogger(__name__)


def require_admin_key(f):
    """All admin endpoints require the X-Admin-Key header to match ADMIN_API_KEY.

    If ADMIN_API_KEY is not configured, access is denied entirely (fail closed).
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        configured_key = os.environ.get('ADMIN_API_KEY')
        if not configured_key:
            return jsonify({'success': False, 'message': 'Admin access is not configured'}), 503
        provided_key = request.headers.get('X-Admin-Key', '')
        if not provided_key or not secrets_compare(provided_key, configured_key):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated


def secrets_compare(a, b):
    import hmac
    return hmac.compare_digest(a.encode(), b.encode())


@admin_bp.route('/logs', methods=['GET'])
@require_admin_key
@limiter.limit("60 per minute")
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

        query = ChatLog.query
        if period == 'week':
            one_week_ago = datetime.utcnow() - timedelta(days=7)
            query = query.filter(ChatLog.created_at >= one_week_ago)

        logs = query.order_by(ChatLog.created_at.desc()).limit(limit or 100).all()

        return jsonify({
            'success': True,
            'count': len(logs),
            'logs': [log.to_dict() for log in logs]
        })

    except Exception:
        logger.exception("Failed to fetch logs")
        return jsonify({'success': False, 'message': 'Internal error'}), 500

@admin_bp.route('/logs/stats', methods=['GET'])
@require_admin_key
@limiter.limit("60 per minute")
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

    except Exception:
        logger.exception("Failed to compute log stats")
        return jsonify({'success': False, 'message': 'Internal error'}), 500

@admin_bp.route('/logs/cleanup', methods=['POST'])
@require_admin_key
@limiter.limit("10 per minute")
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

    except Exception:
        logger.exception("Log cleanup failed")
        return jsonify({'success': False, 'message': 'Internal error'}), 500


@admin_bp.route('/locations', methods=['GET'])
@require_admin_key
@limiter.limit("60 per minute")
def get_locations():
    """
    Get all unique user locations for the map.
    This data persists even after chat logs are cleaned up.
    """
    try:
        locations = UserLocation.get_all_locations()

        return jsonify({
            'success': True,
            'count': len(locations),
            'locations': [loc.to_dict() for loc in locations]
        })

    except Exception:
        logger.exception("Failed to fetch locations")
        return jsonify({'success': False, 'message': 'Internal error'}), 500


@admin_bp.route('/locations/stats', methods=['GET'])
@require_admin_key
@limiter.limit("60 per minute")
def get_location_stats():
    """
    Get statistics about user locations.
    """
    try:
        stats = UserLocation.get_location_stats()

        return jsonify({
            'success': True,
            'stats': stats
        })

    except Exception:
        logger.exception("Failed to compute location stats")
        return jsonify({'success': False, 'message': 'Internal error'}), 500


@admin_bp.route('/locations/import', methods=['POST'])
@require_admin_key
@limiter.limit("5 per minute")
def import_locations():
    """
    Import previously exported location data (the JSON produced by
    GET /locations). Used to restore the map after a database migration.
    Deduplicates against existing records, so it is safe to run repeatedly.
    """
    try:
        data = request.get_json(force=True)
        records = data.get('locations', [])
        if not isinstance(records, list):
            return jsonify({'success': False, 'message': 'Expected a "locations" list'}), 400

        imported, skipped = UserLocation.import_records(records)

        return jsonify({
            'success': True,
            'imported': imported,
            'skipped': skipped
        })

    except Exception:
        logger.exception("Location import failed")
        return jsonify({'success': False, 'message': 'Internal error'}), 500
