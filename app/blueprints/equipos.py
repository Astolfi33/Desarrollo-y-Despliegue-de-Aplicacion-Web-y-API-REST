from flask import Blueprint, render_template, request, redirect, abort, flash, session
from functools import wraps
from handle_files import save_file, delete_file
from models import Equipo
from database import db
from access_control import check_session, check_role

equipos_bp = Blueprint('equipos', __name__, template_folder='../templates')


@equipos_bp.before_request
@check_session
@check_role
def before_request_equipos_bp():
    pass

def load_equipo(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        equipoId = request.view_args.get('equipoId')
        user_id = session['user']['id']
        role = session['user']['role']
        if equipoId is not None:
            query = Equipo.query.filter_by(id=equipoId)
            if role !=  'admin':
                query = query.filter_by(usuario_id=user_id)
            equipo_requested = query.first()
            if equipo_requested is None:
                abort(404)
                
            kwargs['equipo'] = equipo_requested
            del kwargs['equipoId']
        return f(*args, **kwargs)
    return decorated_function


@equipos_bp.route('/', methods=['GET'])
def list():
    nombre = request.args.get('nombre')
    ciudad = request.args.get('ciudad')
    
    query = Equipo.query
    user_id = session['user']['id']
    role = session['user']['role']
    if role != 'admin':
        query = query.filter(Equipo.usuario_id == user_id)
    if nombre is not None:
        query = query.filter(Equipo.nombre.ilike(f'%{nombre}%'))
        
    if ciudad is not None:
        query = query.filter(Equipo.ciudad.ilike(f'%{ciudad}%'))
    
    equipos = query.all()
        
    return render_template('equipos/list.html', equipos=equipos)

@equipos_bp.route('/new', methods=['GET'])
def new():
    return render_template('equipos/new.html')

@equipos_bp.route('/', methods=['POST'])
@save_file
def create(filename):
    capacidad = int(request.form.get('capacidad'))
    if capacidad < 0:
        flash('Error: La capacidad no puede ser negativa', 'error')
        return redirect(request.url)
    
    fundacion = int(request.form.get('fundacion'))
    if fundacion > 2026:
        flash('Error: El año de fundación no puede estar en el futuro', 'error')
        return redirect(request.url)
    
    nuevo_equipo = Equipo(
        nombre=request.form.get('nombre'),
        ciudad=request.form.get('ciudad'),
        ccaa=request.form.get('ccaa'),
        fundacion=fundacion,
        pabellon=request.form.get('pabellon'),
        capacidad=capacidad,
        max_anotador=request.form.get('max_anotador'),
        filename=filename,
        usuario_id=session['user']['id']
    )
    
    db.session.add(nuevo_equipo)
    db.session.commit()
    
    flash('Equipo creado', 'success')
    return redirect('/equipos')


@equipos_bp.route('/<equipoId>', methods=['GET'])
@load_equipo
def show(equipo):
    return render_template('equipos/show.html', equipo=equipo)

@equipos_bp.route('/<equipoId>/edit', methods=['GET'])
@load_equipo
def edit(equipo):   
    return render_template('equipos/edit.html', equipo=equipo)

@equipos_bp.route('/<equipoId>', methods=['PUT'])
@load_equipo
@delete_file
@save_file
def update(equipo, filename):
    equipo.nombre = request.form.get('nombre')
    equipo.ciudad = request.form.get('ciudad')
    equipo.ccaa = request.form.get('ccaa')
    equipo.fundacion = request.form.get('fundacion')
    equipo.pabellon = request.form.get('pabellon')
    equipo.capacidad = request.form.get('capacidad')
    equipo.max_anotador = request.form.get('max_anotador')

    if filename:
        equipo.filename = filename
    
    db.session.commit()
    flash('Equipo editado', 'success')        
    return redirect('/equipos')

@equipos_bp.route('/<equipoId>', methods=['DELETE'])
@load_equipo
@delete_file
def delete(equipo):
    db.session.delete(equipo)
    db.session.commit()
    flash('Equipo borrado', 'success')
    return redirect('/equipos')
        
                
        