from database import db 
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

def generar_uuid():
    return str(uuid.uuid4())

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.String(36), primary_key=True, default=generar_uuid)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), nullable=False, default='user')
    equipos = db.relationship('Equipo', backref='autor')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)