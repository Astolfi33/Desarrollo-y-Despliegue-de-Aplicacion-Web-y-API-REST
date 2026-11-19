from app import db
from models import Usuario

def seedUsuario():
    admin = Usuario(username='admin', email='admin@admin.com', role='admin')
    admin.set_password('1111')
    
    user = Usuario(username='dastolfi', email='dastolfi@user.com', role='user')
    user.set_password('1234')
    
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()
    
    print('Datos insertados correctamente')