import logging
from flask import Blueprint, request, jsonify, session
from src.models.user import db, User
from src.utils.limiter import limiter

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("10 per hour")
def register():
    try:
        data = request.get_json() or {}
        username = (data.get('username') or '').strip()
        email = (data.get('email') or '').strip()
        password = data.get('password') or ''

        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400

        if len(password) < 8:
            return jsonify({'success': False, 'message': 'Password must be at least 8 characters'}), 400

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'}), 409

        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already exists'}), 409

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Log in the user
        session['user_id'] = user.id

        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': user.to_dict()
        })

    except Exception:
        logger.exception("Registration failed")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Registration failed, please try again'}), 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("15 per minute")
def login():
    try:
        data = request.get_json() or {}
        username = (data.get('username') or '').strip()
        password = data.get('password') or ''

        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400

        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if not user or not user.check_password(password):
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

        # Log in the user
        session['user_id'] = user.id

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict()
        })

    except Exception:
        logger.exception("Login failed")
        return jsonify({'success': False, 'message': 'Login failed, please try again'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    user_id = session.get('user_id')
    if user_id:
        user = db.session.get(User, user_id)
        if user:
            return jsonify({
                'authenticated': True,
                'user': user.to_dict()
            })

    return jsonify({'authenticated': False})
