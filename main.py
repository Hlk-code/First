# import uvicorn
# from fastapi import FastAPI
# from sqlalchemy import create_engine, Column, Integer, String, Float
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# # 创建FastAPI实例
# app = FastAPI()
#
# # 定义数据库连接字符串
# DATABASE_URL = "mysql://root:hlk036665@localhost:3306/db"
#
# # 创建数据库引擎和会话
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# # 创建数据模型
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50))
#     email = Column(String(50))
# #第二个表
# class Product(Base):
#     __tablename__ = "products"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     price = Column(Float)
#
# # 创建API路由
# @app.get("/users/{user_id}")
# def read_user(user_id: int):
#     db = SessionLocal()
#     user = db.query(User).filter(User.id == user_id).first()
#     return user
#
#
# @app.post("/users")
# def create_user(name: str, email: str):
#     db = SessionLocal()
#     user = User(username=name, email=email)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user
#
# @app.put("/users/{user_id}")
# def update_user(user_id: int, name: str, email: str):
#     db = SessionLocal()
#     user = db.query(User).filter(User.id == user_id).first()
#     user.username = name
#     user.email = email
#     db.commit()
#     db.refresh(user)
#     return user
#
# @app.delete("/users/{user_id}")
# def delete_user(user_id: int):
#     db = SessionLocal()
#     user = db.query(User).filter(User.id == user_id).first()
#     db.delete(user)
#     db.commit()
#     return {"message": "User deleted"}
#
#
#
# @app.get("/products/{product_id}")
# def read_product(product_id: int):
#     db = SessionLocal()
#     product = db.query(User).filter(Product.id == product_id).first()
#     return product
#
#
#
# # 运行FastAPI应用
# if __name__=='__main__':
#     uvicorn.run('main:app')


import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field

app = FastAPI()

# 数据库连接配置
engine = create_engine("mysql://root:hlk036665@localhost:3306/ceshi", connect_args={"charset": "utf8mb4"})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 跨域配置
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模型类
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    age = Column(Integer)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    price = Column(Integer)

# 请求数据模型
class UserCreate(BaseModel):
    name: str = Field(..., encoding="utf-8")
    age: int

class ItemCreate(BaseModel):
    name: str = Field(..., encoding="utf-8")
    price: int

# 响应数据模型
class UserResponse(BaseModel):
    id: int
    name: str = Field(..., encoding="utf-8")
    age: int

class ItemResponse(BaseModel):
    id: int
    name: str = Field(..., encoding="utf-8")
    price: int

# 创建用户
@app.post("/users/")
def create_user(user: UserCreate):
    db = SessionLocal()
    new_user = User(name=user.name, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(id=new_user.id, name=new_user.name, age=new_user.age)


# 获取用户
@app.get("/users/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=user.id, name=user.name, age=user.age)

# 创建物品
@app.post("/items/")
def create_item(item: ItemCreate):
    db = SessionLocal()
    new_item = Item(name=item.name, price=item.price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return ItemResponse(id=new_item.id, name=new_item.name, price=new_item.price)

# 获取物品
@app.get("/items/{item_id}")
def get_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse(id=item.id, name=item.name, price=item.price)

if __name__=='__main__':
    uvicorn.run('main:app')
