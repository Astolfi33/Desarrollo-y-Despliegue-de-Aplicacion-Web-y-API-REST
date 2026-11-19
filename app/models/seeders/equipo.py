from app import db 
from models import Equipo


def seedEquipo():
    equipo1 = Equipo(nombre='Barça', ciudad='Barcelona', ccaa='Cataluña', fundacion=1942, pabellon='Palau Blaugrana', capacidad=7585, max_anotador='Pablo Álvarez', filename=None)
    equipo2 = Equipo(nombre='Deportivo Liceo', ciudad='A Coruña', ccaa='Galicia', fundacion=1972, pabellon='Pazo dos Deportes de Riazor', capacidad=5000, max_anotador='Arnau Xaus', filename=None)
    equipo3 = Equipo(nombre='Reus Deportiu Virginias', ciudad='Reus', ccaa='Cataluña', fundacion=1909, pabellon='Pavelló Olímpic Municipal de Reus', capacidad=1000, max_anotador='Martí Casas', filename=None)
    db.session.add(equipo1)
    db.session.add(equipo2)
    db.session.add(equipo3)
    db.session.commit()
    print('Datos insertados correctamente')