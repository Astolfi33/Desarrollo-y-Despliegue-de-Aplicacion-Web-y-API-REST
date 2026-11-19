from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from database import db
from models.equipo import Equipo
from models.dtos import EquipoResponseDTO, NewEquipoDTO, EditEquipoDTO
import httpx
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
from logger import logger

bp_api_equipos = Blueprint('api_equipos', __name__)

@cached(ttl=600, cache=Cache.MEMORY, serializer=JsonSerializer())
async def get_weather_data():
    url = 'https://api.open-meteo.com/v1/forecast?latitude=40.4165&longitude=-3.7026&current_weather=true'
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
    return None

@bp_api_equipos.route('/', methods=['GET'])
def get_all():
    logger.info("Se carga la lista de todos los equipos")
    equipos = Equipo.query.all()
    equipos_dto: list[EquipoResponseDTO] = [EquipoResponseDTO.model_validate(equipo) for equipo in equipos]
    response = [equipo.model_dump() for equipo in equipos_dto]
    
    return jsonify(response)

@bp_api_equipos.route('/<int:id>', methods=['GET'])
async def get_by_id(id):
    logger.info(f'Se busca equipo con id: {id}')
    equipo= Equipo.query.get(id)
    if equipo is None:
        logger.error(f'No se encuentra equipo con ID {id}')
        return jsonify({"error": f"Equipo con id {id} no encontrado"}), 404
    equipo.weather = await get_weather_data()
    equipo_dto = EquipoResponseDTO.model_validate(equipo)
    return jsonify(equipo_dto.model_dump())

@bp_api_equipos.route('/', methods=['POST'])
def create():
    body = request.get_json()
    try:
        dto = NewEquipoDTO.model_validate(body)
        model = Equipo(
            nombre=dto.nombre,
            ciudad=dto.ciudad,
            ccaa=dto.ccaa,
            fundacion=dto.fundacion,
            pabellon=dto.pabellon,
            capacidad=dto.capacidad,
            max_anotador=dto.max_anotador,
            usuario_id=dto.usuario_id
        )
        db.session.add(model)
        db.session.commit()
        logger.info(f'Se ha creado el Equipo {model.nombre}')
        response_dto = EquipoResponseDTO.model_validate(model)
        return jsonify(response_dto.model_dump()), 201
        
    except ValidationError as e:
        logger.error(f'Error de validación creando un equipo: {e.errors()}')
        return jsonify(e.errors()), 400
    
    
@bp_api_equipos.route('/<int:id>', methods=['PUT'])
def edit(id):
    logger.info(f'Se busca equipo con id: {id}')
    body = request.get_json()
    
    equipo_query = Equipo.query.get(id)
    if equipo_query is None:
        logger.error(f'No se encuentra equipo con ID {id}')
        return jsonify({"error": f"Equipo {id} not found"}), 404
    
    try:
        dto = EditEquipoDTO.model_validate(body)
        campos_actualizados = dto.model_dump(exclude_unset=True)
        
        for field, value in campos_actualizados.items():
            setattr(equipo_query, field, value)
            
        db.session.commit()
        
        logger.info(f'Se ha actualizado el Equipo {equipo_query.nombre}')
        response_dto = EquipoResponseDTO.model_validate(equipo_query)
        return jsonify(response_dto.model_dump()), 200
        
    except ValidationError as e:
        logger.error(f'Error de validación actualizando un equipo: {e.errors()}')
        return jsonify(e.errors()), 400

@bp_api_equipos.route('/<int:id>', methods=['DELETE'])
def delete(id):
    logger.info(f'Se busca equipo con id: {id}')
    equipo = Equipo.query.get(id)
    
    if equipo is None:
        logger.error(f'No se encuentra equipo con ID {id}')
        return jsonify({"error": f"Equipo {id} not found"}), 404
        
    db.session.delete(equipo)
    db.session.commit()
    
    logger.info(f'Se ha borrado el Equipo {equipo.nombre}')
    return jsonify({"mensaje": "Equipo borrado"})