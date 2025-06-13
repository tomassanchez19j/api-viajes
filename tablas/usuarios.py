import psycopg2
contra = "tomisan19j"
url = f"postgresql://postgres.gtggrdzrgifuqoihvjll:{contra}@aws-0-us-east-2.pooler.supabase.com:6543/postgres"

def connection():
    try:
        conn = psycopg2.connect(url, sslmode='require')
        return conn
    except Exception as e:
        print("error", e)
        return None
class usuario():
    def __init__(self):
        pass
    def insertar_datos_usuarios(self, user_data ):
        
        pass
          
    def recuperar_todos_los_datos_usuarios(self):
        conn = connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios")
            usuarios = cur.fetchall()
            return usuarios
    def recuperar_datos_usuario(self,id):
        conn = connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE ID_usuarios = %s",(id,))
            usuario = cur.fetchone()
            return usuario
    def eliminar_datos_usuarios(self,id):
        conn = connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE ID_usuarios = %s",(id,))



    

     



  