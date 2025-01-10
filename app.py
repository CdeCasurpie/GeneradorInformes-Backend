from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from pathlib import Path
import json
import re

# Importar nuestros módulos
from getStructureModule import analyze_pdf
from singleImageModule import analyze_image
from jsonToMd import convert_json_to_md


app = Flask(__name__, static_url_path='/static', static_folder='static')

# Habilitar CORS para aceptar cualquier dominio
CORS(app)


# Configuración global
SERVER_URL = "http://127.0.0.1:5000"    

# Configuración de carpetas
UPLOAD_FOLDER = Path("static/uploads")
TEMPLATES_FOLDER = Path("static/templates")
IMAGES_FOLDER = Path("static/images")
OUTPUT_FOLDER = Path("static/output")

# Crear carpetas si no existen
for folder in [UPLOAD_FOLDER, TEMPLATES_FOLDER, IMAGES_FOLDER, OUTPUT_FOLDER]:
    folder.mkdir(parents=True, exist_ok=True)

# Configuración de la app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/api/v1/document/analyze', methods=['POST'])
def analyze_document():
    """
    Analiza los archivos iniciales (plantilla y PDF de conocimiento)
    """
    if 'template_file' not in request.files or 'knowledge_file' not in request.files:
        return jsonify({'error': 'Faltan archivos requeridos'}), 400
        
    template_file = request.files['template_file']
    knowledge_file = request.files['knowledge_file']
    
    # Verificar archivos
    if not (template_file and knowledge_file):
        return jsonify({'error': 'No se seleccionaron archivos'}), 400
        
    if not (allowed_file(template_file.filename, {'pdf'}) and 
            allowed_file(knowledge_file.filename, {'pdf'})):
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400
    
    try:
        # Guardar archivos
        template_path = UPLOAD_FOLDER / secure_filename(template_file.filename)
        knowledge_path = UPLOAD_FOLDER / secure_filename(knowledge_file.filename)
        
        template_file.save(template_path)
        knowledge_file.save(knowledge_path)
        
        # Analizar PDF y obtener estructura
        json_structure, markdown_template = analyze_pdf(str(template_path))
        
        # Guardar resultados
        template_filename = template_path.stem
        structure_path = TEMPLATES_FOLDER / f"{template_filename}_structure.json"
        md_path = TEMPLATES_FOLDER / f"{template_filename}.md"
        
        # Guardar JSON y MD
        with open(structure_path, 'w', encoding='utf-8') as f:
            json.dump(json_structure, f, ensure_ascii=False, indent=2)
            
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_template)
        
        return jsonify({
            'template_path': str(md_path),
            'structure_path': str(structure_path)
        })
        
    except Exception as e:
        # Limpieza en caso de error
        for path in [template_path, knowledge_path]:
            if path.exists():
                path.unlink()
        return jsonify({'error': str(e)}), 500

import base64
import uuid
from pathlib import Path

def process_images(data):
    """
    Procesa recursivamente el JSON buscando campos de imagen en base64
    y los guarda como archivos
    """
    if isinstance(data, dict):
        for key in list(data.keys()):
            value = data[key]
            if isinstance(value, str) and (key.endswith('image') or key.endswith('signature')):
                if value.startswith('data:image'):
                    try:
                        # Es una imagen en base64
                        # Extraer el tipo de imagen y los datos
                        image_type = value.split(';')[0].split('/')[1]
                        image_data = value.split(',')[1]
                        image_bytes = base64.b64decode(image_data)
                        
                        # Generar nombre único usando UUID
                        image_filename = f'{uuid.uuid4()}.{image_type}'
                        image_path = IMAGES_FOLDER / image_filename
                        
                        # Guardar imagen
                        with open(image_path, 'wb') as f:
                            f.write(image_bytes)
                        
                        # Actualizar JSON con la ruta relativa
                        data[key] = f'static/images/{image_filename}'
                    except Exception as e:
                        print(f"Error procesando imagen: {str(e)}")
                        # Si hay error, mantener el campo pero vacío
                        data[key] = ''
            elif isinstance(value, (dict, list)):
                data[key] = process_images(value)
    elif isinstance(data, list):
        return [process_images(item) for item in data]
    return data

@app.route('/api/v1/document/generate', methods=['POST'])
def generate_document():
    """
    Genera el documento markdown final con imágenes procesadas
    """
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['form_data', 'template_path', 'structure_path']):
            return jsonify({'error': 'Faltan campos requeridos'}), 400
            
        # 1. Procesar imágenes del form_data y guardarlas
        processed_data = process_images(data['form_data'])
        
        # 2. Analizar imágenes con Vision y actualizar datos
        analyzed_data = analyze_all_images(processed_data)
        
        # 3. Cargar template y generar markdown
        try:
            with open(data['template_path'], 'r', encoding='utf-8') as f:
                template = f.read()
        except Exception as e:
            return jsonify({'error': f'Error leyendo template: {str(e)}'}), 500
            
        markdown_content = convert_json_to_md(analyzed_data, template)
        
        # 4. Reemplazar rutas de imágenes con URLs completas
        while (markdown_content != (eliminate_white_spaces(markdown_content))):
            markdown_content = eliminate_white_spaces(markdown_content)

        # 5. Eliminar espacios en blanco de más
        markdown_content = eliminate_white_spaces(markdown_content)
        
        # 6. Guardar el markdown
        output_path = OUTPUT_FOLDER / f'output_{uuid.uuid4()}.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return jsonify({
            'success': True,
            'markdown_path': str(output_path),
            'processed_data': processed_data  # Opcional: devolver los datos procesados
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def fix_image_paths(markdown_content):
    """
    Reemplaza las rutas relativas de imágenes con URLs completas en las etiquetas <img src="...">
    """
    # Patrón para encontrar imágenes con <img src="ruta">
    pattern = r'<img src="(static/.*?)"'
    
    # Función de reemplazo que añade el dominio
    def replace_path(match):
        image_path = match.group(1)
        return f'<img src="{SERVER_URL}/{image_path}"'

    # Reemplazar todas las coincidencias
    return re.sub(pattern, replace_path, markdown_content)


def eliminate_white_spaces(markdown_content):
    """
    Elimina espacios en blanco de más en el markdown
    """

    # no pueden haber saltos de linea vacios
    pattern = r'\n{2,}' # 2 o más saltos de linea
    return re.sub(pattern, '\n', markdown_content)



def analyze_all_images(data):
    """
    Analiza recursivamente el JSON buscando campos de imagen
    y los analiza con Vision API
    """
    if isinstance(data, dict):
        keys = list(data.keys())
        for key in keys:
            value = data[key]
            if isinstance(value, str) and key.endswith(('image', 'signature')):
                try:
                    if Path(value).exists():  # Es una ruta a imagen
                        image_name = Path(value).name
                        
                        # Definir contexto basado en la clave y estructura
                        context_hints = {
                            'resumen': 'Analizar evidencias y observaciones en obra',
                            'riesgos': 'Identificar riesgos y problemas de seguridad',
                            'conclusion': 'Evaluar estado final y recomendaciones',
                            'signature': 'Verificar firma del supervisor'
                        }
                        
                        # Buscar el mejor contexto basado en la ruta de la clave
                        context_info = next(
                            (hint for context, hint in context_hints.items() if context in key.lower()),
                            "Analizar imagen para informe técnico"
                        )
                        
                        # Analizar imagen
                        analysis_result = analyze_image(value, image_name, context_info)
                        
                        # Añadir resultados al JSON
                        data[f"{key}_analysis"] = analysis_result
                except Exception as e:
                    print(f"Error analizando imagen {value}: {e}")
                    continue
            elif isinstance(value, (dict, list)):
                data[key] = analyze_all_images(value)
    elif isinstance(data, list):
        return [analyze_all_images(item) for item in data]
    return data


if __name__ == '__main__':
    app.run(debug=True)