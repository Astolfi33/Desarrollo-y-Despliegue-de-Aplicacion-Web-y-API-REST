from typing import Optional
from pydantic import BaseModel

class CurrentWeatherUnitsDTO(BaseModel):
    time: str
    interval: str
    temperature: str
    windspeed: str
    winddirection: str
    is_day: str
    weathercode: str

class CurrentWeatherDTO(BaseModel):
    time: str
    interval: int
    temperature: float
    windspeed: float
    winddirection: int
    is_day: int
    weathercode: int

class WeatherResponseDTO(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    current_weather_units: CurrentWeatherUnitsDTO
    current_weather: CurrentWeatherDTO

class NewEquipoDTO(BaseModel):
    nombre: str
    ciudad: str
    ccaa: str
    fundacion: int
    pabellon: str
    capacidad: int
    max_anotador: Optional[str] = None
    usuario_id: Optional[str] = None
    
    model_config = {
        'extra': 'forbid'
    }

class EditEquipoDTO(BaseModel):
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    ccaa: Optional[str] = None
    fundacion: Optional[int] = None
    pabellon: Optional[str] = None
    capacidad: Optional[int] = None
    max_anotador: Optional[str] = None
    usuario_id: Optional[str] = None
    
    model_config = {
        'extra': 'forbid'
    }
    
class EquipoResponseDTO(BaseModel):
    id: int
    nombre: str
    ciudad: str
    ccaa: str
    fundacion: int
    pabellon: str
    capacidad: int
    max_anotador: Optional[str] = None
    usuario_id: Optional[str] = None
    weather: Optional[WeatherResponseDTO] = None
    
    model_config = {
        'from_attributes': True
    }