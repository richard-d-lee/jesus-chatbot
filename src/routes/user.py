from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Conversation
import json

user_bp = Blueprint('user', __name__)

@user_bp.route('/save-conversation', methods=['POST'])
def save_conversation():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'Not authenticated'})
        
        data = request.get_json()
        representation = data.get('representation')
        messages = data.get('messages', [])
        
        if not representation:
            return jsonify({'success': False, 'message': 'Representation is required'})
        
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
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@user_bp.route('/load-conversation/<representation>', methods=['GET'])
def load_conversation(representation):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'Not authenticated'})
        
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
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

