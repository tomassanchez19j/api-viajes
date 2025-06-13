import psycopg2
contra = "tomisan19j"
url = f"postgresql://postgres.gtggrdzrgifuqoihvjll:{contra}@aws-0-us-east-2.pooler.supabase.com:6543/postgres"

def connection():
    try:
        conn = psycopg2.connect(url, ssmodel='require')
        return conn
    except Exception as e:
        print("error", e)
        return None
class vuelo():

    def __init__(self):
        pass
    def crear_tabla(self):
        conn = connection()
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE  IF NOT EXISTS vuelos(
                        ID_vuelos INTEGER PRIMARY KEY AUTOINCREMENT,
                        partida TEXT,
                        destino TEXT,
                        asientos_disponibles INTEGER ,
                        precio INTEGER,
                        fecha_de_salida TEXT,
                        hora_de_salida TEXT
            ) """)
    def insertar_datos_vuelos(self, data):
        conn = connection()
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO vuelos(
                        partida,
                        destino,
                        asientos_disponibles,
                        precio,
                        fecha_de_salida,
                        hora_de_salida)
                        VALUES(
                        %(partida)s,
                        %(destino)s,
                        %(asientos_disponibles)s,
                        %(precio)s,
                        %(fecha_de_salida)s,
                        %(hora_de_salida)s)
            """, data)
    def recuperar_todos_los_datos_vuelos(self):
        conn = connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vuelos")
            vuelo = cur.fetchall
            return vuelo
    def recuperar_datos_vuelos(self,id):
        conn = connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vuelos WHERE ID_vuelos like ?",(id))
            vuelos=cur.fetchone()
            return vuelo
        
    def actualizar_datos_vuelos(self,id,data):
        conn = connection()
        with conn.cursor() as cur:
            cur.execute( f"UPDATE vuelos asientos_disponibles SET  = {data} WHERE ID_vuelos = {id} ")
        
    def eliminar_datos_vuelos(self,id):
        conn = connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM vuelos WHERE ID_vuelos ?",{id})
        

