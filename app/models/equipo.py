from database import db

class Equipo(db.Model):
    __tablename__ = 'equipo'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(255), nullable=False)
    ccaa = db.Column(db.String(255), nullable=False)
    fundacion = db.Column(db.Integer, nullable=False)
    pabellon = db.Column(db.String(255), nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    max_anotador = db.Column(db.String(255), nullable=True) # Por si hay equipos con varios máximos goleadores
    filename = db.Column(db.String(255), nullable=True, unique=True)
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuario.id'), nullable=True)