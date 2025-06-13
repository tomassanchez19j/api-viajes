from pydantic import BaseModel
from typing import Optional
class esquema_usuarios(BaseModel):
    nombre:str
    apellido:str
    dni:int
    pais:str
    email:str
    contraseña:str
class esquema_ventas(BaseModel):
    id_vuelo:int
    id_reserva:int
    id_usuario:int
class esquema_vuelos(BaseModel):
    id:Optional[int]
    partida: str
    destino:str
    asientos_disponibles: int
    precio:int   
    fecha_de_salida: str
    hora_de_salida: str
class esquema_reservas(BaseModel):
    id:Optional[int]
    pais: str
    ciudad: str
    precio: int
class esquema_actualizar_valor_de_campo(BaseModel):
    campo: str