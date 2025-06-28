from fastapi import FastAPI, HTTPException
import psycopg
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from esqumas.esquemasdatos import (
    esquema_usuarios,
    esquema_vuelos,
    esquema_alquileres,
    esquema_ventas_vuelos,
    esquema_ventas_alquileres,
)
from psycopg.rows import dict_row
import csv
import io

contra = "tomisan19j"
url = f"postgresql://postgres.gtggrdzrgifuqoihvjll:{contra}@aws-0-us-east-2.pooler.supabase.com:6543/postgres"

def connection():
    try:
        conn = psycopg.connect(url, sslmode='require', row_factory=dict_row)
        return conn
    except Exception as e:
        print("error", e)
        return None

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# METODOS HTTP DE USUARIOS
@app.post("/api/usuarios")
def insertar_usuarios(user_data: esquema_usuarios):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO usuarios(nombre, apellido, dni, pais, email, contraseña)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_data.nombre, user_data.apellido, user_data.dni,
                  user_data.pais, user_data.email, user_data.contraseña))
    return {"mensaje": "Usuario insertado correctamente"}

@app.get("/api/usuarios/leer")
def recuperar_todos_los_usuarios():
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
    return usuarios

@app.get("/api/usuarios/leer/{id}")
def recuperar_usuario(id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE id_usuarios = %s", (id,))
            usuario = cur.fetchone()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
@app.get("/api/usuarios/leer/{contraseña}")
def recuperar_usuarios_por_contraseña(contraseña: int):
    conn = connection()
    if not conn:
         raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE contraseña = %s", (contraseña,))
            usuario = cur.fetchone()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/api/usuarios/actualizar/{id}")
def actualizar_usuario(user_data: esquema_usuarios, id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE usuarios
                SET nombre = %s, apellido = %s, dni = %s, pais = %s,
                    email = %s, contraseña = %s
                WHERE id_usuarios = %s
            """, (user_data.nombre, user_data.apellido, user_data.dni,
                  user_data.pais, user_data.email, user_data.contraseña, id))
    return {"mensaje": "Usuario actualizado correctamente"}

@app.delete("/api/usuarios/eliminar/{id}")
def eliminar_usuario(id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE id_usuarios = %s", (id,))
    return {"mensaje": "Usuario eliminado correctamente"}

@app.get("/api/usuarios/exportar_csv")
def exportar_usuarios_csv():
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios para exportar")
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=usuarios[0].keys())
    writer.writeheader()
    writer.writerows(usuarios)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=usuarios.csv"})

# METODOS HTTP DE ADMINISTRADORES
@app.get("/api/administradores")
def recuperar_administradores():
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM administradores")
        administradores = cur.fetchall()
    return administradores

# METODOS HTTP DE ALQUILERES
@app.post("/api/alquileres")
def insertar_alquiler(user_data: esquema_alquileres):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO alquileres(tipo_alquiler, precio_dia, dias_disponibles)
                VALUES (%s, %s, %s)
            """, (user_data.tipo_alquiler, user_data.precio_dia, user_data.dias_disponibles))
    return {"mensaje": "Alquiler insertado correctamente"}

@app.get("/api/alquileres/leer")
def recuperar_alquileres():
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM alquileres")
        alquileres = cur.fetchall()
    return alquileres

@app.get("/api/alquileres/leer/{id}")
def recuperar_alquiler(id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM alquileres WHERE id_alquileres = %s", (id,))
            alquiler = cur.fetchone()
    if not alquiler:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")
    return alquiler

@app.put("/api/alquileres/actualizar/{id}")
def actualizar_alquiler(user_data: esquema_alquileres, id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE alquileres
                SET tipo_alquiler = %s, precio_dia = %s, dias_disponibles = %s
                WHERE id_alquileres = %s
            """, (user_data.tipo_alquiler, user_data.precio_dia, user_data.dias_disponibles, id))
    return {"mensaje": "Alquiler actualizado correctamente"}

@app.delete("/api/alquileres/eliminar/{id}")
def eliminar_alquiler(id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM alquileres WHERE id_alquileres = %s", (id,))
    return {"mensaje": "Alquiler eliminado correctamente"}

# METODOS HTTP DE VENTAS DE ALQUILERES
@app.post("/api/ventas_alquileres")
def insertar_venta_alquiler(user_data: esquema_ventas_alquileres):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO venta_de_alquileres(id_alquileres, id_comprador)
                VALUES (%s, %s)
            """, (user_data.id_alquileres, user_data.id_comprador))
    return {"mensaje": "Venta de alquiler insertada correctamente"}

@app.get("/api/ventas_alquileres/leer")
def recuperar_ventas_alquileres():
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM venta_de_alquileres")
        ventas = cur.fetchall()
    return ventas

@app.get("/api/ventas_alquileres/leer/{id}")
def recuperar_venta_alquiler(id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM venta_de_alquileres WHERE id_venta_de_alquileres = %s", (id,))
            venta = cur.fetchone()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta de alquiler no encontrada")
    return venta

@app.put("/api/ventas_alquileres/actualizar/{id}")
def actualizar_venta_alquiler(user_data: esquema_ventas_alquileres, id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE venta_de_alquileres
                SET id_alquileres = %s, id_comprador = %s
                WHERE id_venta_de_alquileres = %s
            """, (user_data.id_alquileres, user_data.id_comprador, id))
    return {"mensaje": "Venta de alquiler actualizada correctamente"}

@app.delete("/api/ventas_alquileres/eliminar/{id}")
def eliminar_venta_alquiler(id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM venta_de_alquileres WHERE id_venta_de_alquileres = %s", (id,))
    return {"mensaje": "Venta de alquiler eliminada correctamente"}

# METODOS HTTP DE VUELOS
@app.post("/api/vuelos")
def insertar_vuelo(user_data: esquema_vuelos):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO vuelos(partida, destino, asientos_disponibles, precio, fecha_de_salida, hora_de_salida)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_data.partida, user_data.destino, user_data.asientos_disponibles,
                  user_data.precio, user_data.fecha_de_salida, user_data.hora_de_salida))
    return {"mensaje": "Vuelo insertado correctamente"}

@app.get("/api/vuelos/leer")
def recuperar_vuelos():
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM vuelos")
        vuelos = cur.fetchall()
    return vuelos

@app.get("/api/vuelos/leer/{id}")
def recuperar_vuelo(id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vuelos WHERE id_vuelos = %s", (id,))
            vuelo = cur.fetchone()
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return vuelo

@app.put("/api/vuelos/actualizar/{id}")
def actualizar_vuelo(user_data: esquema_vuelos, id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE vuelos
                SET partida = %s, destino = %s, asientos_disponibles = %s,
                    precio = %s, fecha_de_salida = %s, hora_de_salida = %s
                WHERE id_vuelos = %s
            """, (user_data.partida, user_data.destino, user_data.asientos_disponibles,
                  user_data.precio, user_data.fecha_de_salida, user_data.hora_de_salida, id))
    return {"mensaje": "Vuelo actualizado correctamente"}

@app.delete("/api/vuelos/eliminar/{id}")
def eliminar_vuelo(id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM vuelos WHERE id_vuelos = %s", (id,))
    return {"mensaje": "Vuelo eliminado correctamente"}

# METODOS HTTP DE VENTAS DE VUELOS
@app.post("/api/ventas_de_vuelos")
def insertar_venta_vuelo(user_data: esquema_ventas_vuelos):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO ventas_de_vuelos(id_vuelo, id_comprador, fecha_compra, metodo_pago, total)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_data.id_vuelo, user_data.id_comprador, user_data.fecha_compra, user_data.metodo_compra, user_data.total))
    return {"mensaje": "Venta de vuelo insertada correctamente"}

@app.get("/api/ventas_de_vuelos/leer")
def recuperar_ventas_vuelos():
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM ventas_de_vuelos")
        ventas = cur.fetchall()
    return ventas

@app.get("/api/ventas_de_vuelos/leer/{id}")
def recuperar_venta_vuelo(id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM ventas_de_vuelos WHERE id_ventas_de_vuelos = %s", (id,))
            venta = cur.fetchone()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta de vuelo no encontrada")
    return venta

@app.put("/api/ventas_de_vuelos/actualizar/{id}")
def actualizar_venta_vuelo(user_data: esquema_ventas_vuelos, id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE ventas_de_vuelos
                SET id_vuelo = %s, id_comprador = %s
                WHERE id_ventas_de_vuelos = %s
            """, (user_data.id_vuelo, user_data.id_comprador, id))
    return {"mensaje": "Venta de vuelo actualizada correctamente"}

@app.delete("/api/ventas_de_vuelos/eliminar/{id}")
def eliminar_venta_vuelo(id: int):
    conn = connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM ventas_de_vuelos WHERE id_ventas_de_vuelos = %s", (id,))
    return {"mensaje": "Venta de vuelo eliminada correctamente"}
