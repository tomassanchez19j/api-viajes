from pydantic import BaseModel
from typing import Optional
class esquema_usuarios(BaseModel):
    nombre:str
    apellido:str
    dni:int
    pais:str
    email:str
    contraseña:str
class esquema_ventas_vuelos(BaseModel):
    id_vuelo:int
    id_comprador:int
    fecha_compra: str
    hora_compra: str
    monto_total: int
class esquema_vuelos(BaseModel):
    partida: str
    destino:str
    asientos_disponibles: int
    precio:int   
    fecha_de_salida: str
    hora_de_salida: str
class esquema_ventas_alquileres(BaseModel):
    id_alquileres: int
    id_comprador: int 
class esquema_alquileres(BaseModel):
    tipo_alquiler: str
    precio_dia: int
    dias_disponibles:int

