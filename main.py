from fastapi import FastAPI
import psycopg2
from fastapi.middleware.cors import CORSMiddleware
from esqumas.esquemasdatos import esquema_usuarios, esquema_vuelos,esquema_alquileres,esquema_ventas_vuelos,esquema_ventas_alquileres
contra = "tomisan19j"
url = f"postgresql://postgres.gtggrdzrgifuqoihvjll:{contra}@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
def connection():
    try:
        conn = psycopg2.connect(url, sslmode='require')
        return conn
    except Exception as e:
        print("error", e)
        return None

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
        usuarios = cur.fetchall()
    return usuarios
@app.get("/api/usuarios/leer/{id}")
def recuperar_usuarios(id: int):
    conn = connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE id_usuarios = (%s);",(id,))
            usuario = cur.fetchone()
        return usuario
@app.put("/api/usuarios/actualizar/{id}")
def actualizar_usuarios(user_data:esquema_usuarios ,id:int):
    try:
        conn = connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE usuarios SET nombre = %s, apellido= %s, dni= %s,pais=%s,email=%s,contraseña=%s WHERE id_usuarios = %s;", (user_data.nombre, user_data.apellido,user_data.dni,user_data.pais,user_data.email,user_data.contraseña, id)) 
                return {"mensaje": "usuario actualizado correctamente"}
       
    except Exception as e:
        return {"error": str(e)}
@app.delete("/api/usuarios/eliminar/{id}")
def eliminar_usuarios(id:int):
   
    try:
        conn = connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE id_usuarios = (%s);",(id,))
            return {"se":"elimino"}
    except Exception as e:
        return {"error": str(e)}






#METODOS HTTP DE ventas_de_vueloS

@app.get("/api/ventas_de_vuelos/leer")
def recuperar_todas_las_ventas_de_vuelos():
    conn = connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM ventas_de_vuelos")
        ventas_de_vuelos = cur.fetchall()
    return ventas_de_vuelos
@app.get("/api/ventas_de_vuelos/leer/{id}")
def recuperar_ventas_de_vuelos(id:int):

    conn = connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM ventas_de_vuelos WHERE id_ventas_de_vuelos = (%s);",(id,))
            ventas_de_vuelo = cur.fetchone()
        return ventas_de_vuelo
@app.put("api/ventas_de_vuelos/actualizar/{id}")
def eliminar_vuelos(user_data:esquema_ventas_vuelos,id:int):
    try:
        conn = connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE venta_de_vuelos SET id_vuelo = %s, id_comprador = %s WHERE id_venta_de_vuelos = %s;", (user_data.id_vuelo, user_data.id_comprador, id)) 
                return {"mensaje": "usuario actualizado correctamente"}
       
    except Exception as e:
        return {"error": str(e)}
@app.delete("/git/ventas_de_vuelos/eliminar/{id}")
def eliminar_ventas_de_vuelos(id:int):
    try:
        conn = connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM ventas_de_vuelos WHERE id_ventas_de_vuelos = (%s);",(id,))
            return {"se":"elimino"}
    except Exception as e:
        return {"error": str(e)}
    





#METODOS HTTP DE VUELOS
@app.post("/api/vuelos")
def insertar_vuelos(user_data: esquema_vuelos):
    conn = connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO vuelos(
                            partida,
                            destino,
                            asientos_disponibles,
                            precio,
                            fecha_de_salida,
                            hora_de_salida,
                            id_comprador)
                            VALUES(%s,%s,%s,%s,%s,%s,%s)
                """, (user_data.partida,user_data.destino,user_data.asientos_disponibles,user_data.precio,user_data.fecha_de_salida,user_data.hora_de_salida,user_data.id_comprador))
        return {"vuelo_guardado":"si"}
    except Exception as e:
        print(e)
@app.get("/api/vuelos/leer")
def recuperar_todos_los_vuelos():
    conn = connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM vuelos")
        vuelos = cur.fetchall()
    return vuelos 
@app.get("/api/vuelos/leer/{id}")
def recuperar_vuelos(id:str):
    conn = connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vuelos WHERE id_vuelos = (%s);",(id,))
            vuelo = cur.fetchone()
        return vuelo
@app.put("/api/vuelos/actualizar/{id}")
def actualizar_asientos_disponibles(user_data:esquema_vuelos,id:int):
    try:
        conn = connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE vuelos SET partida = %s, destino = %s, asientos_disponibles= %s,precio=%s,fecha_de_salida=%s,hora_de_salida=%s WHERE id_vuelos = %s;", (user_data.partida, user_data.destino,user_data.asientos_disponibles,user_data.precio,user_data.fecha_de_salida,user_data.hora_de_salida, id)) 
                return {"mensaje": "usuario actualizado correctamente"}
       
    except Exception as e:
        return {"error": str(e)}
@app.delete("/api/vuelos/eliminar/{id}")
def eliminar_vuelos(id:str):
    try:
        conn = connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM vuelos WHERE id_vuelos = (%s);",(id,))
            return {"se":"elimino"}
    except Exception as e:
        return {"error": str(e)}





#METODOS HTTP DE VENTAS DE ALQUILERES   
@app.post("/api/ventas_alquileres")
def insertar_ventas_alquileres(user_data: esquema_ventas_alquileres):
    conn = connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO venta_de_alquileres(id_alquileres,id_comprador)
                            VALUES(%s,%s)
                """, (user_data.id_alquileres,user_data.id_comprador,))
        return {"reserva_guardado":"si"}
    except Exception as e:
        print(e)
@app.get("/api/ventas_alquileres/leer")
def recuperar_todas_las_ventas_alquileres():
    conn = connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM venta_de_alquileres")
        ventas= cur.fetchall()
    return ventas
@app.get("/api/ventas_alquileres/leer/{id}")
def recuperar_ventas_alquileres(id:str):
    conn = connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM venta_de_alquileres WHERE id_venta_de_alquileres = (%s);",(id,))
            venta = cur.fetchone()
        return venta
@app.put("/api/ventas_alquileres/actualizar/{id}")
def actualizar_ventas_alquileres_disponibles(user_data:esquema_ventas_alquileres,id:int):
    try:
        conn = connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE venta_de_alquileres SET id_alquileres = %s, id_comprador = %s WHERE id_venta_de_alquileres = %s;", (user_data.id_alquileres, user_data.id_comprador, id)) 
                return {"mensaje": "usuario actualizado correctamente"}
       
    except Exception as e:
        return {"error": str(e)}
@app.delete("/api/ventas_alquileres/eliminar/{id}")
def eliminar_ventas_alquileres(id:str):
    try:
        conn = connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM ventas_de_alquileres WHERE id_ventas_de_alquileres = (%s);",(id,))
            return {"se":"elimino"}
    except Exception as e:
        return {"error": str(e)}



#METODOS HTTP DE ALQUILERES
@app.post("/api/alquileres")
def insertar_alquileres(user_data: esquema_alquileres):
    conn = connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO alquileres(tipo_alquiler,precio_dia,dias_disponibles)
                            VALUES(%s,%s,%s)
                """, (user_data.tipo_alquiler,user_data.precio_dia,user_data.dias_disponibles))
        return {"reserva_guardado":"si"}
    except Exception as e:
        print(e)
@app.get("/api/alquileres/leer")
def recuperar_todos_los_alquileres():
    conn = connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM alquileres")
        alquiler= cur.fetchall()
    return alquiler
@app.get("/api/alquileres/leer/{id}")
def recuperar_alquileres(id:str):
    conn = connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM alquileres WHERE id_alquileres = (%s);",(id,))
            alquiler = cur.fetchone()
        return alquiler
@app.put("/api/alquileres/actualizar/{id}")
def actualizar_alquileres_disponibles(user_data:esquema_alquileres,id:int):
    try:
        conn = connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE alquileres SET tipo_alquiler = %s, precio_dia = %s, dias_disponibles= %s WHERE id_alquileres = %s;", (user_data.tipo_alquiler, user_data.precio_dia,user_data.dias_disponibles, id)) 
                return {"mensaje": "usuario actualizado correctamente"}
       
    except Exception as e:
        return {"error": str(e)}
@app.delete("/api/alquileres/eliminar/{id}")
def eliminr_alquileres(id:str):
    try:
        conn = connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM alquileres WHERE id_alquileres = (%s);",(id,))
            return {"se":"elimino"}
    except Exception as e:
        return {"error": str(e)}



    
    