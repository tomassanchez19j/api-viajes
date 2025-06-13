import psycopg2
class reserva():
    conn = None
    def __init__(self):
        try:
            dns = "postgresql://usuariosdb_vmnf_user:Eoy4bOkKAeNouZs8aoI3EO4TumIjWOVs@dpg-d14brfuuk2gs73andh0g-a.oregon-postgres.render.com/usuariosdb_vmnf"
            self.conn = psycopg2.connect(dns)
        except psycopg2.OperationalError as err:
            print(err)
    def crear_tabla(self):
        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE  IF NOT EXISTS reservas(
                        ID_reservas INTEGER PRIMARY KEY AUTOINCREMENT,
                        pais TEXT,
                        ciudad TEXT,
                        precio INTEGER
            ) """)
        self.conn.commit()
    def insertar_datos_reservas(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""INSERT INTO ventas_de_reservas(
                        pais,
                        ciudad,
                        precio)
                        VALUES(
                        %(pais)s,
                        %(ciudad)s,
                        %(precio)s,
            """, data)
        self.conn.commit()
    def recuperar_todos_los_datos_reservas(self):
        with self.conn.cursor() as cur:
            reservas = cur.execute("SELECT * FROM reservas")
            return reservas.fetchall()
    def recuperar_datos_reservas(self,id):
        with self.conn.cursor() as cur:
            reservas = cur.execute("SELECT * FROM reservas WHERE ID_reservas like ?",(id))
            return reservas.fetchone()
        self.conn.commit()
    def actualizar_datos_reservas(self,id,data):
        with self.conn.cursor() as cur:
            cur.execute( f"UPDATE reservas asientos_disponibles SET  = {data} WHERE ID_reservas = {id} ")
        self.conn.commit()
    def eliminar_datos_reservas(self,id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM reservas WHERE ID_reservas ?",{id})
        self.conn.commit()

