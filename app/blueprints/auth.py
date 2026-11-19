from flask import Blueprint, request, redirect, render_template, session, flash
from models import Usuario
from database import db

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if Usuario.query.filter_by(email=email).first():
        flash('El email ya está registrado', 'error')
        return redirect('/auth/register')
    
    new_user = Usuario(
        username=username,
        email=email
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    flash('Registro exitoso, ahora puedes iniciar sesión', 'success')
    return redirect('/auth/login')

@auth_bp.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = Usuario.query.filter_by(email=email).first()
    if user and user.check_password(password):
        session['user'] = {
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'id': user.id
        }
        flash('Inicio de sesión exitoso', 'success')
        return redirect('/')
    else:
        flash('Correo o contraseña incorrectos', 'error')
        return redirect('/auth/login')
    
    
@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sesión cerrada correctamente', 'success')
    return redirect('/')