from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# Asegúrate de que Neo4jConnection está implementado
from database import Neo4jConnection
# Asegúrate de que Usuario está implementado como un modelo de Pydantic
from models import Usuario

app = FastAPI()

# Conexión a Neo4j
neo4j_conn = Neo4jConnection(
    uri="bolt://54.172.132.64:7687", user="neo4j", password="azimuths-bundle-wartime"
)

# Validar los datos de un nuevo usuario con Pydantic
nuevo_usuario = Usuario(nombre="Clara", edad=32, email="clara@example.com")

# Insertar en Neo4j
query = """
CREATE (u:Usuario {nombre: $nombre, edad: $edad, email: $email})
RETURN u
"""
neo4j_conn.query(query, parameters=nuevo_usuario.model_dump())


@app.get("/")
def read_root():
    return {"message": "Bienvenido a tu crudsito con FastAPI, Neo4j y Stripe"}


@app.post("/usuarios/")
def create_usuario(usuario: Usuario):
    query = """
    CREATE (u:Usuario {nombre: $nombre, edad: $edad, email: $email})
    RETURN u
    """
    result = neo4j_conn.query(query, parameters=usuario.model_dump())
    return {"usuario": usuario}


@app.get("/usuarios/{nombre}")
def read_usuario(nombre: str):
    query = """
    MATCH (u:Usuario {nombre: $nombre})
    RETURN u.nombre AS nombre, u.edad AS edad, u.email AS email
    """
    result = neo4j_conn.query(query, parameters={"nombre": nombre})
    record = result.single()
    if record:
        return {"nombre": record["nombre"], "edad": record["edad"], "email": record["email"]}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.put("/usuarios/{nombre}")
def update_usuario(nombre: str, usuario: Usuario):
    query = """
    MATCH (u:Usuario {nombre: $nombre})
    SET u.edad = $edad, u.email = $email
    RETURN u
    """
    result = neo4j_conn.query(query, parameters={
        "nombre": nombre, "edad": usuario.edad, "email": usuario.email
    })
    if result.single():
        return {"mensaje": "Usuario actualizado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.delete("/usuarios/{nombre}")
def delete_usuario(nombre: str):
    query = """
    MATCH (u:Usuario {nombre: $nombre})
    DELETE u
    """
    result = neo4j_conn.query(query, parameters={"nombre": nombre})
    if result.summary().counters.nodes_deleted > 0:
        return {"mensaje": "Usuario eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
