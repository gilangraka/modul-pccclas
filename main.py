from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="api-perpustakaan"
)

# Create a cursor object
cursor = mydb.cursor()

class Buku(BaseModel):
    judul: Optional[str] = None
    penulis: Optional[str] = None
    tahun: Optional[int] = None
    id_status: Optional[int] = None

app = FastAPI()

@app.get("/buku")
def get_all_buku():
    query = "SELECT * FROM ref_buku"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@app.get("/buku/{id_buku}")
def get_by_id(id_buku: int):
    query = "SELECT * FROM ref_buku WHERE id = %s"
    values = (id_buku,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    return result

@app.post("/buku")
def post_buku(buku:Buku):
    query = "INSERT INTO ref_buku (judul_buku, penulis, tahun_terbit, id_status) VALUES (%s, %s, %s, %s)"
    values = (buku.judul, buku.penulis, buku.tahun, buku.id_status)
    cursor.execute(query, values)
    mydb.commit()
    return {"message" : "Berhasil menyimpan data buku"}

@app.put("/buku/{id_buku}")
def update_buku(id_buku: int, buku: Buku):
    query_parts = []
    values = []
    
    if buku.judul is not None:
        query_parts.append("judul_buku = %s")
        values.append(buku.judul)
    
    if buku.penulis is not None:
        query_parts.append("penulis = %s")
        values.append(buku.penulis)
    
    if buku.tahun is not None:
        query_parts.append("tahun_terbit = %s")
        values.append(buku.tahun)
    
    if buku.id_status is not None:
        query_parts.append("id_status = %s")
        values.append(buku.id_status)
    
    if not query_parts:
        return {"message": "Tidak ada data yang diperbarui"}
    
    query = f"UPDATE ref_buku SET {', '.join(query_parts)} WHERE id = %s"
    values.append(id_buku)
    
    cursor.execute(query, tuple(values))
    mydb.commit()
    
    return {"message": "Berhasil memperbarui data buku"}

@app.delete("/buku/{id_buku}")
def delete_buku(id_buku: int) :
    query = "DELETE FROM ref_buku WHERE id = %s"
    values = (id_buku,)
    cursor.execute(query, values)
    mydb.commit()
    return {"message" : "Data buku berhasil dihapus"}