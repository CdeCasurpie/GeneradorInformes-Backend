from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import jsonify, request
import os
import uuid

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Después de actualizar el modelo, necesitarás ejecutar una migración de base de datos
# o recrear la base de datos para que incluya el nuevo campo is_admins

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Verificar si el usuario existe usando el token como ID
        user = User.query.get(token)
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
            
        request.user_id = token
        return f(*args, **kwargs)
    return decorated_function

def add_auth_routes(app):
    @app.route('/api/v1/auth/register', methods=['POST'])
    def register():
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing username or password'}), 400
            
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
            
        user = User(username=data['username'])
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': user.id,
            'token': user.id
        })

    @app.route('/api/v1/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing username or password'}), 400
            
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # si es el admin se le envia la señal
        if user.is_admin == True:
            return jsonify({
                'token': user.id,
                'user_id': user.id,
                'is_admin': True
            })
            
        return jsonify({
            'token': user.id,
            'user_id': user.id
        })

    @app.route('/api/v1/document/files', methods=['GET'])
    @login_required
    def get_user_files():
        user_id = request.user_id
        
        templates = []
        structures = []
        knowledge_files = []
        
        template_path = app.config['TEMPLATES_FOLDER']
        for file in os.listdir(template_path):
            if file.startswith(f"{user_id}_"):
                if file.endswith('.md'):
                    templates.append(file.replace(f"{user_id}_", ""))
                elif file.endswith('.json'):
                    structures.append(file.replace(f"{user_id}_", ""))
                    
        upload_path = app.config['UPLOAD_FOLDER']
        for file in os.listdir(upload_path):
            if file.startswith(f"{user_id}_"):
                knowledge_files.append(file.replace(f"{user_id}_", ""))
                
        return jsonify({
            'templates': templates,
            'structures': structures,
            'knowledge_files': knowledge_files
        })