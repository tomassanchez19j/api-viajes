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
class venta():
    def __init__(self):
        pass
    def insertar_datos_ventas(self, data):
        with self.conn.cursor() as cur:
          cur.execute("""INSERT INTO ventas(
                        compra,
                        fecha,
                        monto)
                        VALUES(
                        %(compra)s,
                        %(fecha)s,
                        %(monto)s)
            """, data)
    def recuperar_todos_los_datos_ventas(self):
        with self.conn.cursor() as cur:
            ventas = cur.execute("SELECT * FROM ventas")
            return ventas.fetchall()
    def recuperar_datos_ventas(self,id):
        with self.conn.cursor() as cur:
            venta = cur.execute("SELECT * FROM ventas WHERE ID_venta like ?",(id))
            return venta.fetchone()
        self.conn.commit()
    def eliminar_datos_ventas(self,id):
        with self.conn.cursor() as cur:
              cur.execute("DELETE FROM ventas WHERE ID_ventas ?",{id})
        self.conn.commit()




