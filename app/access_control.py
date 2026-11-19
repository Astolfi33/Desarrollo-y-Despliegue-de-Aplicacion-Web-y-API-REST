from flask import request, session, redirect, abort
from functools import wraps

def check_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/auth/login')
        return f(*args, **kwargs)
    return decorated_function

permissions = {
    "admin": [
        "equipos.list",
        "equipos.new",
        "equipos.create",
        "equipos.show",
        "equipos.edit",
        "equipos.update",
        "equipos.delete",
        "usuarios.list",
        "usuarios.new",
        "usuarios.create",
        "usuarios.show",
        "usuarios.edit",
        "usuarios.update",
        "usuarios.delete"
    ],
    "user": [
        "equipos.list",
        "equipos.new",
        "equipos.create",
        "equipos.show",
        "equipos.edit",
        "equipos.update",
        "equipos.delete",
    ]
}

def check_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        endpoint = request.endpoint
        role = session["user"]["role"]
        
        if endpoint not in permissions[role]:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function