from flask import jsonify, request
from db_model import User, db
from functools import wraps
import os
from pathlib import Path



OUTPUT_FOLDER = Path("static/output")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Verificar si el usuario existe y es admin
        user = User.query.get(token)
        if not user or not user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
            
        return f(*args, **kwargs)
    return decorated_function

def add_admin_routes(app):
    # Ruta para crear usuarios (solo admin)
    @app.route('/api/v1/admin/users', methods=['POST'])
    @admin_required
    def create_user():
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
            'user_id': user.id
        })

    # Ruta para obtener todos los reportes
    @app.route('/api/v1/admin/reports', methods=['GET'])
    @admin_required
    def get_all_reports():
        try:
            # Obtener todos los archivos en la carpeta de output
            output_dir = Path("static/output")
            reports = []
            
            # Recorrer todos los archivos en la carpeta de output
            for file in output_dir.glob('*.md'):
                # Obtener información del archivo
                stat = file.stat()
                
                # Obtener el usuario que creó el archivo (si está disponible)
                user_id = file.stem.split('_')[1] if '_' in file.stem else 'Unknown'
                user = User.query.get(user_id)
                username = user.username if user else 'Unknown User'


                #la primmeria lineaea de cada archivo es el nombre del archivo

                firss_line = "No se ha encontrado el nombre del archivo"
                with open(file, 'r') as f:
                    first_line = f.readline()
                    if not first_line.startswith("#"):
                        continue
                

                
                reports.append({
                    'filename': first_line[1:].strip(),
                    'created_at': stat.st_mtime,  # timestamp de modificación
                    'created_by': username,
                    'url': f"/static/output/{file.name}"
                })
            
            # Ordenar por fecha de creación (más reciente primero)
            reports.sort(key=lambda x: x['created_at'], reverse=True)
            
            return jsonify({
                'reports': reports
            })
            
        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        
    @app.route('/api/v1/admin/users', methods=['GET'])
    @admin_required
    def get_all_users():
        users = User.query.all()
        return jsonify({
            'users': [
                {
                    'id': user.id,
                    'username': user.username,
                } for user in users
            ]
        })

    return app