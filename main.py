from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from esqumas.esquemasdatos import esquema_usuarios, esquema_vuelos, esquema_ventas, esquema_actualizar_valor_de_campo,esquema_reservas
#from tablas.usuarios import usuario
from tablas.ventas import venta
from tablas.vuelos import vuelo
from tablas.reservas import reserva
from tablas.usuarios import connection
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
conn = connection()

if conn:
    print("✅")
    conn.close()
else:
    print("❌")

#METODOS HTTP DE USUARIOS
@app.post("/api/usuarios")
def insertar_usuarios(user_data: esquema_usuarios):
    conn = connection()
    print(conn)
    with conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO usuarios(
                        nombre,
                        apellido,
                        dni,
                        pais,
                        email,
                        contraseña)
                        VALUES(%s,%s,%s,%s,%s,%s)
                
            """,(user_data.nombre,user_data.apellido,user_data.dni,user_data.pais,user_data.email,user_data.contraseña))
            return {"hola":"mundo"}
@app.get("/api/usuarios/leer")
def recuperar_todos_los_usuarios():
    conn = connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchone()
    return usuarios
@app.get("/api/usuarios/leer/{id}")
async def recuperar_usuarios(id: int):
    conn = connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE id = (%s);",(id,))
            usuario = cur.fetchone()
        return usuario
#METODOS HTTP DE VENTAS
@app.post("/api/ventas")
def ingresar_ventas(user_data: esquema_ventas):
    conn = connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO ventas(
                            id_vuelo,
                            id_reserva,
                            id_usuario)
                            VALUES(%s,%s,%s)
                """, (user_data.id_vuelo,user_data.id_reserva,user_data.id_usuario))
            return {"hola":"mundo"}
    except Exception as e:
        print(e)
#METODOS HTTP DE VUELOS
@app.post("/api/vuelos")
def ingresar_vuelos(user_data: esquema_vuelos):
    data = user_data.model_dump()
    data.pop("id")
    conn.insertar_datos_vuelos(data)
@app.get("/api/vuelos/leer")
def recuperar_todos_los_vuelos():
    items_vuelos=[]
    for data in conn.recuperar_todos_los_datos_vuelos():
        diccionario_vuelos={}
        diccionario_vuelos["id"] = data[0]
        diccionario_vuelos["partida"] = data[1]
        diccionario_vuelos["destino"] = data[2]
        diccionario_vuelos["asientos_disponibles"] = data[3]
        diccionario_vuelos["precio"] = data[4]
        diccionario_vuelos["fecha_de_salida"] = data[5]
        diccionario_vuelos["hora_de_salida"] = data[6]
        items_vuelos.append(diccionario_vuelos)
    return items_vuelos
@app.get("/api/vuelos/leer/{id}")
def recuperar_vuelos(id:str):
    data = conn.recuperar_datos_vuelos(id)
    diccionario_vuelos={}
    diccionario_vuelos["id"] = data[0]
    diccionario_vuelos["partida"] = data[1]
    diccionario_vuelos["destino"] = data[2]
    diccionario_vuelos["asientos_disponibles"] = data[3]
    diccionario_vuelos["precio"] = data[4]
    diccionario_vuelos["fecha_de_salida"] = data[5]
    diccionario_vuelos["hora_de_salida"] = data[6]
    return diccionario_vuelos
@app.put("/api/vuelos/actualizar/{id}")
def actualizar_asientos_disponibles(id:str,user_data:esquema_actualizar_valor_de_campo):
    data = user_data.model_dump()
    conn.actualizar_datos_vuelos(id,data)
@app.delete("/api/vuelos/borrar/{id}")
def eliminar_vuelos(id:str):
    conn.eliminar_datos_vuelos(id) 
#METODOS HTTP DE RESERVAS
@app.post("/api/reservas")
def ingresar_reservas(user_data: esquema_reservas):
    data = user_data.model_dump()
    conn.insertar_datos_reservas(data)
@app.get("/api/reservas/leer")
def recuperar_todas_las_reservas():
    items_resevas=[]
    for data in conn.recuperar_todos_los_datos_reservas():
        diccionario_reservas={}
        diccionario_reservas["id"] = data[0]
        diccionario_reservas["pais"] = data[1]
        diccionario_reservas["ciudad"] = data[2]
        diccionario_reservas["precio"] = data[3]
        items_resevas.append(diccionario_reservas)
    return items_resevas
@app.get("/api/reservas/leer/{id}")
def recuperar_reservas(id:str):
    diccionario_reservas={}
    data = conn.recuperar_datos_reservas(id)
    diccionario_reservas["id"] = data[0]
    diccionario_reservas["pais"] = data[1]
    diccionario_reservas["ciudad"] = data[2]
    diccionario_reservas["precio"] = data[3]
    return diccionario_reservas
@app.put("/api/reservas/actualizar/{id}")
def actualizar_reservas_disponibles(id:str,user_data:esquema_actualizar_valor_de_campo):
    data = user_data.model_dump()
    conn.actualizar_datos_reservas(id,data)
@app.delete("/api/reservas/eliminar/{id}")
def eliminar_reservas(id:str):
    conn.eliminar_datos_reservas(id)




    
    