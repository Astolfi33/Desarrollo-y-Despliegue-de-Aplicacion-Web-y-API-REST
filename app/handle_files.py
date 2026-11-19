import os
import uuid
from functools import wraps
from flask import request, redirect, flash
from app import app
from PIL import Image

def allowed_file(filename): # Comprueba si el fichero tiene una extensión permitida
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_file(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        file = request.files['file'] if 'file' in request.files else None # Comprueba si se ha subido un fichero
        kwargs['filename'] = None
        if file:
            if not allowed_file(file.filename): # Comprueba si la extensión del fichero es permitida
                flash('Archivo no permitido. Formatos permitidos: png, jpg, jpeg', 'error')
                return redirect(request.url)
            
            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            file.seek(0,0)
            if file_length > 5*1024*1024:
                flash('El fichero supera los 5MB', 'error')
                return redirect(request.url)
            
            filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}" if file else None # Genera un nombre único para el fichero
            kwargs['filename'] = filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Guarda el fichero en la carpeta de imágenes usando la libreria os
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            path_thumbnail = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
            img_pillow = Image.open(path)
            img_pillow.thumbnail((150, 150))
            img_pillow.save(path_thumbnail)
        return f(*args, **kwargs)
    return decorated_function


def delete_file(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        filename = kwargs['equipo'].filename     
        
        if request.method == "PUT":
            if 'file' not in request.files or request.files['file'].filename == "":
                return f(*args, **kwargs) 
        
        if filename and 'http' not in filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path): # Comprueba si el fichero existe
                os.remove(file_path) # Borra el fichero
                thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
                if os.path.exists(thumb_path):
                    os.remove(thumb_path)
        return f(*args, **kwargs)
    return decorated_function