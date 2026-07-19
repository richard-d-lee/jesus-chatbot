import json
import logging
from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Conversation

user_bp = Blueprint('user', __name__)
logger = logging.getLogger(__name__)

@user_bp.route('/save-conversation', methods=['POST'])
def save_conversation():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401

        data = request.get_json() or {}
        representation = data.get('representation')
        messages = data.get('messages', [])

        if not representation:
            return jsonify({'success': False, 'message': 'Representation is required'}), 400

        # Find existing conversation or create new one
        conversation = Conversation.query.filter_by(
            user_id=user_id,
            representation=representation
        ).first()

        if conversation:
            conversation.messages = json.dumps(messages)
        else:
            conversation = Conversation(
                user_id=user_id,
                representation=representation,
                messages=json.dumps(messages)
            )
            db.session.add(conversation)

        db.session.commit()

        return jsonify({'success': True, 'message': 'Conversation saved'})

    except Exception:
        logger.exception("Failed to save conversation")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to save conversation'}), 500

@user_bp.route('/load-conversation/<representation>', methods=['GET'])
def load_conversation(representation):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'Not authenticated'}), 401

        conversation = Conversation.query.filter_by(
            user_id=user_id,
            representation=representation
        ).first()

        if conversation:
            messages = json.loads(conversation.messages)
            return jsonify({
                'success': True,
                'messages': messages
            })
        else:
            return jsonify({
                'success': True,
                'messages': []
            })

    except Exception:
        logger.exception("Failed to load conversation")
        return jsonify({'success': False, 'message': 'Failed to load conversation'}), 500
