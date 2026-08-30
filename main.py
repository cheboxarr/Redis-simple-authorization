import os
from dotenv import load_dotenv
import uuid
from fastapi import FastAPI, Request, Response, HTTPException, Cookie
from redis.asyncio import Redis
from server import users_table, metadata
from sqlalchemy import create_engine, select, Table, Column, Integer, String, ForeignKey, insert, update
from fastapi import FastAPI, HTTPException, Response, Request, Depends
from pydantic import BaseModel, Field


load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


engine_url = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(engine_url, echo=False)



metadata.create_all(engine)

app = FastAPI()

origins = [
    'http://localhost:8080',
    'http://127.0.0.1:8000'
]



redis = Redis(host="redis", port=6379, decode_responses=True)


class User(BaseModel):
    id: int
    name: str

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя")

class UserLogin(BaseModel):
    name: str



@app.post('/users/add', response_model=User)
async def add_user(user: UserCreate):
    try:
        with engine.connect() as conn:
            existing = conn.execute(
                select(users_table).where(users_table.c.name == user.name)
            ).fetchone()
            
            if existing:
                raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
            query = users_table.insert().values(
                name=user.name
            )
            conn.execute(query)
            conn.commit()
            last_id_query = select(users_table.c.id).where(users_table.c.name == user.name)
            row = conn.execute(last_id_query).fetchone()
            
            inserted_id = row[0] if row else 1
            return User(id=inserted_id, name=user.name)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"ошибка регистрации: {e}", flush=True)
        raise HTTPException(status_code=500, detail="Ошибка при регистрации на стороне сервера")








@app.post("/auth/login")
async def login(user: UserLogin, response: Response):
    try:
        with engine.connect() as conn:
            existing = conn.execute(
            select(users_table).where(users_table.c.name == user.name)
            ).fetchone()
            if not existing:
                raise HTTPException(status_code=400, detail="Неверное имя пользователя")
        
            session_id = str(uuid.uuid4())
    

            await redis.set(f"session:{session_id}", user.name, ex=1800)
    
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True, 
                samesite="lax" 
                )
    
            return {"message": "Успешный вход!"}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"ошибка регистрации: {e}", flush=True)
        raise HTTPException(status_code=500, detail="Ошибка при регистрации на стороне сервера")
        

@app.get("/users/me")
async def get_me(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=401, detail="Вы не авторизованы (нет куки)")


    user = await redis.get(f"session:{session_id}")
    
    if not user:
        raise HTTPException(status_code=401, detail="Сессия истекла или не существует")
        
    return {"user": user, "status": "authorized", "info": "Данные из Redis"}

@app.post("/auth/logout")
async def logout(response: Response, session_id: str = Cookie(None)):
    if session_id:
        await redis.delete(f"session:{session_id}")
        

    response.delete_cookie(key="session_id")
    return {"message": "Успешный выход"}