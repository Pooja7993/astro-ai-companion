"""
Web UI for Astro AI Companion
Flask application with family management interface
"""

import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from sqlalchemy.orm import Session
from datetime import datetime
import json

from src.config.database import get_db, init_database
from src.models.user_models import User, Family, BirthChart, Prediction
from src.services.astrology_service import astrology_service
from src.services.openrouter_service import openrouter_service

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize database
init_database()

@app.route('/')
def index():
    """Main dashboard."""
    return render_template('index.html')

@app.route('/family')
def family_dashboard():
    """Family management dashboard."""
    return render_template('family.html')

@app.route('/api/register', methods=['POST'])
def register_user():
    """Register a new family member."""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['telegram_id', 'first_name', 'last_name', 'birth_date', 'birth_time', 'birth_place']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        db = next(get_db())
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.telegram_id == data['telegram_id']).first()
        if existing_user:
            return jsonify({'error': 'User already registered'}), 400
        
        # Create new user
        new_user = User(
            telegram_id=data['telegram_id'],
            telegram_chat_id=data.get('telegram_chat_id', data['telegram_id']),
            first_name=data['first_name'],
            middle_name=data.get('middle_name'),
            last_name=data['last_name'],
            birth_date=data['birth_date'],
            birth_time=data['birth_time'],
            birth_place=data['birth_place'],
            relationship_to_head=data.get('relationship', 'member')
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Calculate birth chart asynchronously
        socketio.start_background_task(calculate_birth_chart_async, new_user.id)
        
        return jsonify({
            'success': True,
            'user_id': new_user.id,
            'message': 'User registered successfully. Calculating astrological profile...'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/family/<int:family_id>/members')
def get_family_members(family_id):
    """Get all family members."""
    try:
        db = next(get_db())
        members = db.query(User).filter(User.family_id == family_id).all()
        
        result = []
        for member in members:
            birth_chart = db.query(BirthChart).filter(BirthChart.user_id == member.id).first()
            result.append({
                'id': member.id,
                'name': member.full_name,
                'relationship': member.relationship_to_head,
                'birth_date': member.birth_date,
                'sun_sign': birth_chart.sun_sign if birth_chart else None,
                'moon_sign': birth_chart.moon_sign if birth_chart else None,
                'life_path_number': birth_chart.life_path_number if birth_chart else None
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/<int:user_id>/guidance')
def get_user_guidance(user_id):
    """Get unified guidance for a user."""
    try:
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        birth_chart = db.query(BirthChart).filter(BirthChart.user_id == user_id).first()
        
        if not birth_chart:
            return jsonify({'error': 'Birth chart not calculated yet'}), 404
        
        # Get latest prediction or generate new one
        today = datetime.now().strftime('%Y-%m-%d')
        prediction = db.query(Prediction).filter(
            Prediction.user_id == user_id,
            Prediction.prediction_date == today,
            Prediction.prediction_type == 'daily'
        ).first()
        
        if not prediction:
            # Generate new prediction
            socketio.start_background_task(generate_prediction_async, user_id, 'daily')
            return jsonify({'message': 'Generating new guidance...'}), 202
        
        return jsonify({
            'unified_guidance': prediction.unified_guidance,
            'vedic_guidance': prediction.vedic_guidance,
            'numerology_guidance': prediction.numerology_guidance,
            'lal_kitab_guidance': prediction.lal_kitab_guidance,
            'remedies': json.loads(prediction.remedies) if prediction.remedies else []
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Chat endpoint for natural language interaction."""
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message')
        
        if not user_id or not message:
            return jsonify({'error': 'Missing user_id or message'}), 400
        
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        birth_chart = db.query(BirthChart).filter(BirthChart.user_id == user_id).first()
        
        # Prepare context
        context = f"""
        User: {user.full_name}
        Sun Sign: {birth_chart.sun_sign if birth_chart else 'Unknown'}
        Moon Sign: {birth_chart.moon_sign if birth_chart else 'Unknown'}
        Life Path Number: {birth_chart.life_path_number if birth_chart else 'Unknown'}
        """
        
        system_prompt = f"""You are a personal astrology companion for {user.full_name}. 
        You combine Vedic astrology, numerology, and Lal Kitab to provide personalized guidance.
        
        User's Profile: {context}
        
        Respond naturally and conversationally. Provide practical, positive guidance."""
        
        response = await openrouter_service.generate_response(message, system_prompt)
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_birth_chart_async(user_id):
    """Calculate birth chart asynchronously."""
    try:
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return
        
        # Default coordinates (Mumbai)
        latitude = 19.0760
        longitude = 72.8777
        
        # Calculate birth chart
        birth_chart = astrology_service.calculate_birth_chart(
            user.birth_date, user.birth_time, user.birth_place, latitude, longitude
        )
        
        # Calculate numerology
        numerology = astrology_service.calculate_numerology(
            user.birth_date, user.full_name
        )
        
        # Generate Lal Kitab analysis
        lal_kitab = astrology_service.generate_lal_kitab_analysis(birth_chart)
        
        # Store in database
        chart_record = BirthChart(
            user_id=user.id,
            sun_sign=birth_chart.get('planets', {}).get('Sun', {}).get('sign'),
            moon_sign=birth_chart.get('planets', {}).get('Moon', {}).get('sign'),
            ascendant=birth_chart.get('ascendant'),
            nakshatra=birth_chart.get('nakshatra', {}).get('name'),
            planetary_positions=str(birth_chart.get('planets', {})),
            house_positions=str(birth_chart.get('houses', {})),
            aspects=str(birth_chart.get('aspects', [])),
            life_path_number=numerology.get('life_path_number'),
            destiny_number=numerology.get('destiny_number'),
            soul_number=numerology.get('soul_number'),
            lal_kitab_analysis=str(lal_kitab)
        )
        
        db.add(chart_record)
        db.commit()
        
        # Emit completion event
        socketio.emit('birth_chart_ready', {'user_id': user_id})
        
    except Exception as e:
        print(f"Error calculating birth chart: {e}")

def generate_prediction_async(user_id, prediction_type):
    """Generate prediction asynchronously."""
    try:
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        birth_chart = db.query(BirthChart).filter(BirthChart.user_id == user_id).first()
        
        if not user or not birth_chart:
            return
        
        # Generate unified guidance
        guidance = astrology_service.generate_unified_guidance(
            user.__dict__,
            eval(birth_chart.planetary_positions) if birth_chart.planetary_positions else {},
            {
                'life_path_number': birth_chart.life_path_number,
                'destiny_number': birth_chart.destiny_number,
                'soul_number': birth_chart.soul_number
            },
            eval(birth_chart.lal_kitab_analysis) if birth_chart.lal_kitab_analysis else {},
            prediction_type
        )
        
        # Store prediction
        prediction = Prediction(
            user_id=user_id,
            prediction_type=prediction_type,
            prediction_date=datetime.now().strftime('%Y-%m-%d'),
            unified_guidance=guidance,
            remedies=json.dumps([])  # Add remedies logic here
        )
        
        db.add(prediction)
        db.commit()
        
        # Emit completion event
        socketio.emit('prediction_ready', {
            'user_id': user_id,
            'prediction_type': prediction_type,
            'guidance': guidance
        })
        
    except Exception as e:
        print(f"Error generating prediction: {e}")

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)