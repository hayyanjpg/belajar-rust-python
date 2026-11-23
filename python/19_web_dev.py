"""
19_web_dev.py - Web Development dengan Flask dan FastAPI

Tahap 5: Spesialisasi - Web Development
Materi: flask, fastapi, routing, REST API, template, request/response
"""

# ============================================================================
# FLASK - Micro web framework
# ============================================================================

def demo_flask():
    """
    Contoh struktur aplikasi Flask.
    Install: pip install flask
    Jalankan: flask run (setelah export FLASK_APP=app_flask.py)
    """
    flask_code = '''
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Data dummy
users = [
    {"id": 1, "nama": "Budi", "email": "budi@example.com"},
    {"id": 2, "nama": "Siti", "email": "siti@example.com"},
    {"id": 3, "nama": "Joko", "email": "joko@example.com"},
]

@app.route('/')
def home():
    return render_template('index.html', users=users)

@app.route('/about')
def about():
    return "<h1>About Page</h1><p>Belajar Flask dan Python</p>"

@app.route('/users')
def get_users():
    return jsonify(users)

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User tidak ditemukan"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "nama": data.get("nama"),
        "email": data.get("email")
    }
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)
'''
    print("=== KONSTRUKSI APLIKASI FLASK ===")
    print(flask_code)
    print("Simpan kode di atas sebagai app_flask.py, lalu jalankan dengan 'flask run'")


# ============================================================================
# FASTAPI - Modern, fast web framework
# ============================================================================

def demo_fastapi():
    """
    Contoh struktur aplikasi FastAPI.
    Install: pip install fastapi uvicorn
    Jalankan: uvicorn app_fastapi:app --reload
    """
    fastapi_code = '''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Belajar FastAPI", version="1.0.0")

# Model data
class User(BaseModel):
    id: int
    nama: str
    email: str

class UserCreate(BaseModel):
    nama: str
    email: str

# Data dummy
users_db = [
    User(id=1, nama="Budi", email="budi@example.com"),
    User(id=2, nama="Siti", email="siti@example.com"),
    User(id=3, nama="Joko", email="joko@example.com"),
]


@app.get("/")
def read_root():
    return {"message": "Selamat datang di Belajar FastAPI"}


@app.get("/users", response_model=List[User])
def get_users():
    return users_db


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User tidak ditemukan")


@app.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate):
    new_id = max(u.id for u in users_db) + 1
    new_user = User(id=new_id, **user.model_dump())
    users_db.append(new_user)
    return new_user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserCreate):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            updated = User(id=user_id, **user_update.model_dump())
            users_db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="User tidak ditemukan")


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(i)
            return {"message": "User berhasil dihapus"}
    raise HTTPException(status_code=404, detail="User tidak ditemukan")
'''
    print("\n=== KONSTRUKSI APLIKASI FASTAPI ===")
    print(fastapi_code)
    print("Simpan kode di atas sebagai app_fastapi.py, lalu jalankan dengan 'uvicorn app_fastapi:app --reload'")
    print("Dokumentasi otomatis tersedia di http://localhost:8000/docs")


def latihan_flask():
    print("\n=== LATIHAN FLASK ===")
    print("Buat route '/hello/<nama>' yang mengembalikan 'Halo {nama}!'")
    print("Contoh response: Halo Budi!")


def latihan_fastapi():
    print("\n=== LATIHAN FASTAPI ===")
    print("Buat endpoint '/produk' dengan method GET yang mengembalikan daftar produk")
    print("Setiap produk memiliki: id, nama, harga, stok")


if __name__ == '__main__':
    demo_flask()
    demo_fastapi()
    latihan_flask()
    latihan_fastapi()
