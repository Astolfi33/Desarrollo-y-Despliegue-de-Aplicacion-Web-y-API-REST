from flask import Blueprint, render_template, request, redirect, abort, flash
from functools import wraps
from models import Usuario
from database import db
from access_control import check_session, check_role

usuarios_bp = Blueprint('usuarios', __name__, template_folder='../templates')


@usuarios_bp.before_request
@check_session
@check_role
def before_request_usuarios_bp():
    pass

def load_usuario(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        usuarioId = request.view_args.get('usuarioId')
        if usuarioId is not None:
            usuario_requested = Usuario.query.get(usuarioId)
            if usuario_requested is None:
                abort(404)
            
            kwargs['usuario'] = usuario_requested
            del kwargs['usuarioId']
        return f(*args, **kwargs)
    return decorated_function


@usuarios_bp.route('/', methods=['GET'])
def list():
    usuarios = Usuario.query.all()
    return render_template('usuarios/list.html', usuarios=usuarios)

@usuarios_bp.route('/new', methods=['GET'])
def new():
    return render_template('usuarios/new.html')

@usuarios_bp.route('/', methods=['POST'])
def create():
    nuevo_usuario = Usuario(
        username=request.form.get('username'),
        email=request.form.get('email')
    )
     
    password_raw = request.form.get('password')
    if password_raw:
        nuevo_usuario.set_password(password_raw)
        
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    flash('Usuario creado', 'success')
    return redirect('/usuarios')

@usuarios_bp.route('/<usuarioId>/edit', methods=['GET'])
@load_usuario
def edit(usuario):
    return render_template('usuarios/edit.html', usuario=usuario)

@usuarios_bp.route('/<usuarioId>', methods=['PUT'])
@load_usuario
def update(usuario):
    usuario.username = request.form.get('username')
    usuario.email = request.form.get('email')
    new_raw = request.form.get('password')
    if new_raw:
        usuario.set_password(new_raw)
    db.session.commit()
    flash('Usuario editado', 'success')
    return redirect('/usuarios')

@usuarios_bp.route('/<usuarioId>', methods=['DELETE'])
@load_usuario
def delete(usuario):
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario borrado', 'success')
    return redirect('/usuarios')